import os
import os.path

base_path = os.environ.get("USERPROFILE")
if base_path is None:
    base_path = os.environ.get("HOME")
if base_path is None:
    base_path = os.curdir

app_dir = os.path.join(base_path, "KHRR")
os.makedirs(app_dir, exist_ok=True)

logs_dir = os.path.join(app_dir, "logs")
os.makedirs(logs_dir, exist_ok=True)

projects_dir = os.path.join(app_dir, "projects")
os.makedirs(projects_dir, exist_ok=True)

solvers_dir = os.path.join(app_dir, "solvers")
os.makedirs(solvers_dir, exist_ok=True)

def get_project_path(project_name : str) -> str:
    return os.path.join(projects_dir, project_name)

def get_project_ini_path(project_name : str) -> str:
    project_dir = get_project_path(project_name)
    ini_dir = os.path.join(project_dir, "ini")
    return ini_dir


def create_new_project_directory(project_name : str) -> str:
    project_dir = get_project_path(project_name)

    if (os.path.exists(project_dir)):
        raise FileExistsError(f"Проект с именем '{project_name}' уже существует.")

    os.makedirs(project_dir)

    return project_dir
    
def create_ini_directory(project_name : str) -> str:
    project_dir = get_project_path(project_name)

    if (not os.path.exists(project_dir)):
        raise FileExistsError(f"Проект с именем '{project_name}' не существует.")

    ini_dir = os.path.join(project_dir, "ini")
    os.makedirs(ini_dir, exist_ok=True)

    return ini_dir