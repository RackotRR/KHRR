#!/usr/bin/env python3
"""
Скрипт-обёртка для запуска дочернего процесса.

Запускается из Streamlit через subprocess.Popen(start_new_session=True),
после чего становится независимым процессом. Пишет состояние в файлы,
чтобы Streamlit мог наблюдать за ним даже после перезапуска.

Использование:
    python launcher.py --task-id mytask --log-dir ./run -- <command> [args...]
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def atomic_write(path: Path, content: str) -> None:
    """Атомарная запись, чтобы читатель не увидел записанный файл."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


class Launcher:
    def __init__(self, task_id: str, log_dir: Path, command: list[str]):
        self.task_id = task_id
        self.log_dir = log_dir
        self.command = command

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.pid_file = log_dir / f"{task_id}.pid"
        self.status_file = log_dir / f"{task_id}.status"
        self.exitcode_file = log_dir / f"{task_id}.exitcode"
        self.started_file = log_dir / f"{task_id}.started"
        self.log_file = log_dir / f"{task_id}.log"

        self.proc: subprocess.Popen | None = None
        self.log_fh = None
        self._terminating = False

    def _write_status(self, status: str, **extra) -> None:
        payload = {
            "task_id": self.task_id,
            "status": status,
            "pid": self.proc.pid if self.proc else None,
            "command": self.command,
            "updated_at": now_iso(),
            **extra,
        }
        atomic_write(self.status_file, json.dumps(payload, ensure_ascii=False, indent=2))

    def _install_signal_handlers(self) -> None:
        """При SIGTERM/SIGINT — корректно гасим дочерний процесс."""
        def handler(signum, frame):
            self._terminating = True
            self._write_status("terminating", signal=signum)
            if self.proc and self.proc.poll() is None:
                try:
                    # Сначала мягко
                    self.proc.terminate()
                    try:
                        self.proc.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        # Затем жёстко
                        self.proc.kill()
                        self.proc.wait(timeout=5)
                except ProcessLookupError:
                    pass
            sys.exit(143 if signum == signal.SIGTERM else 130)

        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

    def run(self) -> int:
        self._install_signal_handlers()

        # Записываем свой PID — это PID обёртки, не воркера.
        # Он же — «владелец» задачи с точки зрения Streamlit.
        atomic_write(self.pid_file, str(os.getpid()))
        atomic_write(self.started_file, now_iso())
        self._write_status("starting")

        # Открываем лог один раз. Воркер пишет и в stdout, и в stderr — мержим.
        self.log_fh = open(self.log_file, "a", encoding="utf-8", buffering=1)

        self.log_fh.write(f"\n=== [{now_iso()}] launcher started (pid={os.getpid()}) ===\n")
        self.log_fh.write(f"=== command: {' '.join(self.command)} ===\n\n")
        self.log_fh.flush()

        try:
            # Запускаем воркер в новой сессии, чтобы Ctrl+C в терминале
            # (если он есть) не долетел до него. Обёртка сама управляет.
            self.proc = subprocess.Popen(
                self.command,
                stdout=self.log_fh,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
        except Exception as e:
            self.log_fh.write(f"\n=== failed to start: {e} ===\n")
            self.log_fh.flush()
            self._write_status("failed_to_start", error=str(e))
            atomic_write(self.exitcode_file, "127")
            return 127

        self._write_status("running", worker_pid=self.proc.pid)

        # Ждём завершения. wait() здесь безопасен, потому что мы не читаем
        # из PIPE — вывод идёт напрямую в файл.
        returncode = self.proc.wait()

        self.log_fh.write(f"\n=== [{now_iso()}] finished with exit code {returncode} ===\n")
        self.log_fh.flush()
        self.log_fh.close()

        atomic_write(self.exitcode_file, str(returncode))
        self._write_status(
            "finished" if returncode == 0 else "failed",
            returncode=returncode,
        )

        # Свой PID-файл можно удалить — задача завершена.
        try:
            self.pid_file.unlink()
        except FileNotFoundError:
            pass

        return returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Task launcher wrapper")
    parser.add_argument("--task-id", required=True, help="Уникальный ID задачи")
    parser.add_argument("--log-dir", default="./run", help="Директория для state-файлов")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Команда после --")
    args = parser.parse_args()

    # argparse.REMAINDER оставляет ведущий '--', убираем его
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]

    if not args.command:
        parser.error("Не указана команда для запуска (после --)")

    return args


if __name__ == "__main__":
    args = parse_args()
    launcher = Launcher(
        task_id=args.task_id,
        log_dir=Path(args.log_dir).resolve(),
        command=args.command,
    )
    sys.exit(launcher.run())