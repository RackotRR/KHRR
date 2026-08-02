from . import filesystem_handler as FilesystemHandler
import sqlite3
import os
import pandas as pd

GENERAL_DATABASE_NAME = "khrr.db"
PROJECT_DATABASE_NAME = "project.khrrp"

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