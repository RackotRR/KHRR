import streamlit as st
import os
import json
import pandas as pd
import utils.filesystem_handler as FilesystemHandler
import utils.db_handler as DbHandler



NUMBER_FORMAT="%.5f"

@st.dialog("Новый ini-файл компоненты")
def new_particles_ini_dialog(project_name : str):
    particles_ini_name = st.text_input("Название файла компоненты")
    no_ini_name = len(particles_ini_name) == 0

    uploaded_file = st.file_uploader("Файл компоненты", type=["txt", ""])
    no_uploaded_file = uploaded_file is None

    create_particles_ini = st.button(
        "Создать",
        use_container_width=True,
        disabled=no_ini_name or no_uploaded_file
    )
    if create_particles_ini:
        try:
            FilesystemHandler.create_particles_ini_file(
                project_name,
                particles_ini_name,
                uploaded_file.getbuffer()
            )
            st.rerun()

        except FileExistsError as ex:
            st.error(f"Ошибка создания файла компоненты. { ex }")

MASS_STAR_ID = "mass_star"
MASS_DARK_ID = "mass_dark"
SOFT_STAR_ID = "soft_star"
SOFT_DARK_ID = "soft_dark"
INI_FILE_STAR_ID = "ini_file_star"
INI_FILE_DARK_ID = "ini_file_dark"

def make_ini_params(project_name : str, ini_params : dict):

    # одна галактика
    with st.expander("Начальные условия (упрощённый режим)", expanded=True):

        col_star, col_dark = st.columns(2)

        ini_params[MASS_STAR_ID] = col_star.number_input(
            "Масса звёздной компоненты",
            value=ini_params.get(MASS_STAR_ID, 1.0),
            format=NUMBER_FORMAT,
            help="Безразмерная масса"
        )
        ini_params[MASS_DARK_ID] = col_dark.number_input(
            "Масса тёмной компоненты",
            value=ini_params.get(MASS_DARK_ID, 1.0),
            format=NUMBER_FORMAT,
            help="Безразмерная масса"
        )

        ini_params[SOFT_STAR_ID] = col_star.number_input(
            "Сглаживание звёздной компоненты",
            value=ini_params.get(SOFT_STAR_ID, 0.004),
            format=NUMBER_FORMAT
        )
        ini_params[SOFT_DARK_ID] = col_dark.number_input(
            "Сглаживание тёмной компоненты",
            value=ini_params.get(SOFT_DARK_ID, 0.004),
            format=NUMBER_FORMAT
        )

        def to_relative_ini_path(abs_ini_path : str | None) -> str | None:
            if abs_ini_path is None:
                return None
            else:
                filename = os.path.basename(abs_ini_path)
                name_without_ext = os.path.splitext(filename)[0]
                return name_without_ext

        def to_absolute_ini_path(relative_ini_path : str | None) -> str | None:
            if relative_ini_path is None:
                return None
            else:
                return os.path.join(
                    FilesystemHandler.get_project_ini_path(project_name),
                    relative_ini_path + ".txt")

        ini_options = [None] + FilesystemHandler.scan_for_particles_ini(project_name)
        star_ini_index = ini_options.index(to_relative_ini_path(ini_params.get(INI_FILE_STAR_ID)))
        dark_ini_index = ini_options.index(to_relative_ini_path(ini_params.get(INI_FILE_DARK_ID)))


        ini_star_selection = col_star.selectbox(
            "Файл звёздной компоненты",
            index=star_ini_index,
            options=ini_options)
        init_dark_selection = col_dark.selectbox(
            "Файл тёмной компоненты",
            index=dark_ini_index,
            options=ini_options)


        ini_params[INI_FILE_STAR_ID] = to_absolute_ini_path(ini_star_selection)
        ini_params[INI_FILE_DARK_ID] = to_absolute_ini_path(init_dark_selection)

        if st.button("Импорт файла с частицами", use_container_width=True):
            new_particles_ini_dialog(project_name)

    return ini_params

def make_ini_params_table(ini_params : dict):
    data_params = pd.DataFrame([{
        "Масса звёздной компоненты": ini_params.get(MASS_STAR_ID),
        "Масса тёмной компоненты": ini_params.get(MASS_DARK_ID),
        "Сглаживание звёздной компоненты": ini_params.get(SOFT_STAR_ID),
        "Сглаживание тёмной компоненты": ini_params.get(SOFT_DARK_ID),
        "Файл звёздной компоненты": ini_params.get(INI_FILE_STAR_ID),
        "Файл тёмной компоненты": ini_params.get(INI_FILE_DARK_ID),
    }])
    st.table(data_params.transpose(), hide_header=True)

TIME_MAX_ID = "time_max"
DT_SAVE_ID = "dt_save"
DT_DYNAMICS_ID = "dt_dynamics"
def make_sim_params(sim_params : dict):

    with st.expander("Параметры симуляции", expanded=True):
        sim_params[TIME_MAX_ID] = st.number_input(
            "Время симуляции",
            value=sim_params.get(TIME_MAX_ID, 1.0),
            format=NUMBER_FORMAT,
            help="Безразмерное время"
        )
        sim_params[DT_SAVE_ID] = st.number_input(
            "Шаг сохранения",
            value=sim_params.get(DT_SAVE_ID, 0.01),
            format=NUMBER_FORMAT,
            help="Безразмерное время"
        )
        sim_params[DT_DYNAMICS_ID] = st.number_input(
            "Шаг интегрирования",
            value=sim_params.get(DT_DYNAMICS_ID, 0.001),
            format=NUMBER_FORMAT,
            help="Безразмерное время"
        )

    return sim_params

def make_sim_params_table(sim_params : dict):
    data_params = pd.DataFrame([{
            "Время симуляции": sim_params.get("time_max"),
            "Шаг сохранения": sim_params.get("dt_save"),
            "Шаг интегрирования": sim_params.get("dt_dynamics"),
        }]
    )
    st.table(data_params.transpose(), hide_header=True)



def make_run_params():

    with st.expander("Параметры запуска", expanded=True):
        solvers = FilesystemHandler.scan_for_solvers()
        st.selectbox("Используемый солвер", options=solvers)

def read_calculation_ini_params(
        project_name : str,
        calculation_name : str
    ):

    calculation_path = FilesystemHandler.get_project_calculation_path(project_name, calculation_name)
    calculation_ini_path = os.path.join(calculation_path, DbHandler.CALCULATION_INI_DATABASE_NAME)

    ini_params = {}
    if os.path.exists(calculation_ini_path):
        with open(calculation_ini_path) as f:
            ini_params = json.load(f)
    else:
        st.error(f"В расчёте отсутствует {DbHandler.CALCULATION_INI_DATABASE_NAME}")

    return ini_params

def read_calculation_sim_params(
        project_name : str,
        calculation_name : str
    ):

    calculation_path = FilesystemHandler.get_project_calculation_path(project_name, calculation_name)
    calculation_sim_path = os.path.join(calculation_path, DbHandler.CALCULATION_SIM_DATABASE_NAME)

    sim_params = {}
    if os.path.exists(calculation_sim_path):
        with open(calculation_sim_path) as f:
            sim_params = json.load(f)
    else:
        st.error(f"В расчёте отсутствует {DbHandler.CALCULATION_SIM_DATABASE_NAME}")

    return sim_params