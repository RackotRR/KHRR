from . import filesystem_handler as FilesystemHandler
import sqlite3
import os
import pandas as pd
import json

GENERAL_DATABASE_NAME = "rrgsim.db"
PROJECT_DATABASE_NAME = "project.db"
CALCULATION_PARAMS_DATABASE_NAME = "params.json"

def get_general_db_path() -> str:
    app_path = FilesystemHandler.app_dir
    db_path = os.path.join(app_path, GENERAL_DATABASE_NAME)
    return db_path

def init_general_db():
    db_path = get_general_db_path()
    with sqlite3.connect(db_path) as conn:
        pass





def init_project_db(project_name : str):
    project_path = FilesystemHandler.get_project_path(project_name)
    db_path = os.path.join(project_path, PROJECT_DATABASE_NAME)


def fill_calculation_db(
        project_name : str,
        calculation_name : str,
        params_dict : dict
    ):
    calculation_path = FilesystemHandler.get_project_calculation_path(project_name, calculation_name)
    params_path = os.path.join(calculation_path, CALCULATION_PARAMS_DATABASE_NAME)

    with open(params_path, "w", encoding="utf-8") as f:
        json.dump(params_dict, f, ensure_ascii=False, indent=4)