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

def check_project_exists(project_name : str):
    project_dir = get_project_path(project_name)

    if not os.path.exists(project_dir):
        raise FileExistsError(f"Проект с именем '{project_name}' не существует.")

def check_project_not_exist(project_name : str):
    project_dir = get_project_path(project_name)

    if os.path.exists(project_dir):
        raise FileExistsError(f"Проект с именем '{project_name}' уже существует.")

def get_project_path(project_name : str) -> str:
    return os.path.join(projects_dir, project_name)

def get_project_ini_path(project_name : str) -> str:
    return os.path.join(get_project_path(project_name), "ini")

def get_project_calcs_path(project_name : str) -> str:
    return os.path.join(get_project_path(project_name), "calcs")

def get_project_calculation_path(project_name : str, calculation_name : str) -> str:
    return os.path.join(get_project_calcs_path(project_name), calculation_name)

def create_new_project_directory(project_name : str) -> str:
    check_project_not_exist(project_name)
    project_dir = get_project_path(project_name)

    os.makedirs(project_dir)
    return project_dir
    
def create_ini_directory(project_name : str) -> str:
    check_project_exists(project_name)

    ini_dir = get_project_ini_path(project_name)
    os.makedirs(ini_dir, exist_ok=True)

    return ini_dir

def create_calculations_directory(project_name : str) -> str:
    check_project_exists(project_name)

    calculations_dir = get_project_calcs_path(project_name)
    os.makedirs(calculations_dir, exist_ok=True)

    return calculations_dir

def create_new_calculation_directory(project_name : str, calculation_name : str) -> str:
    create_calculations_directory(project_name)

    calc_dir = get_project_calculation_path(project_name, calculation_name)
    if os.path.exists(calc_dir):
        raise FileExistsError(f"Расчёт с именем '{calculation_name}' уже существует.")

    os.makedirs(calc_dir)
    return calc_dir

def scan_for_solvers() -> list[str]:
    solvers_raw = os.listdir(solvers_dir)
    solvers = []
    for solver_path in solvers_raw:
        file_name, _ = os.path.splitext(solver_path)
        solvers.append(file_name)

    return solvers