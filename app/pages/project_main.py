import streamlit as st
import pages.common.sidebar as CommonSidebar
import pages.common.navigation as CommonNavigation
import utils.db_handler as DbHandler
import utils.filesystem_handler as FilesystemHandler
import os

st.title("KHRR")

if not "project_name" in st.query_params:
    st.error("В параметрах запроса не указано название проекта.")
    if (st.button(label="Home", use_container_width=True)):
        CommonNavigation.switch_to_select_project()
    st.stop()
PROJECT_NAME = st.query_params["project_name"]

DbHandler.init_project_db(PROJECT_NAME)
ini_dir = FilesystemHandler.create_ini_directory(PROJECT_NAME)
calculations_dir = FilesystemHandler.create_calculations_directory(PROJECT_NAME)
calculations = os.listdir(calculations_dir)


NUMBER_FORMAT="%.5f"

st.header(f"Проект '{PROJECT_NAME}'")

CommonSidebar.make_sidebar()
         
    # with st.container(border=True):
    #     st.markdown("#### Начальные условия")

    #     # нужно уметь выбирать частицы не все (например, убрать тёмную материю)
    #     # или выбрать другое начальное приближение (не все галактики)

    #     st.selectbox("Доступные", [])
    #     st.button("Импорт галактики")


    #     # test
    #     with st.container(border=True):
    #         st.markdown("##### Параметры галактики")


    #         count_star_particles = 200_000
    #         count_dark_particles = 450_000

    #         with st.expander("Исходные данные по частицам"):
    #             st.selectbox(
    #                 "Источник данных по частицам звёздного вещества",
    #                 options=[
    #                     "Загруженные данные",
    #                     "Импорт",
    #                     "Результаты расчёта"
    #                 ]
    #             )

    #         # численные параметры галактики
    #         col_star, col_dark = st.columns(2)

    #         use_star_particles = col_star.toggle("Использовать частицы звёздного вещества", value=True)
    #         use_dark_particles = col_dark.toggle("Использовать частицы тёмного вещества", value=True)

    #         col_star.write(f"Частиц звёздного вещества: {count_star_particles if use_star_particles else 0}")
    #         col_dark.write(f"Частиц тёмного вещества: {count_dark_particles if use_dark_particles else 0}")
            
    #         col_star.number_input(
    #             "Масса звёздной компоненты", 
    #             value=1.0, 
    #             format=NUMBER_FORMAT, 
    #             help="Безразмерная масса",
    #             disabled=not use_star_particles
    #         )
    #         col_dark.number_input(
    #             "Масса тёмной компоненты", 
    #             value=1.0, 
    #             format=NUMBER_FORMAT, 
    #             help="Безразмерная масса",
    #             disabled=not use_dark_particles
    #         )

    #         col_star.number_input(
    #             "Сглаживание звёздной компоненты", 
    #             value=0.004, 
    #             format=NUMBER_FORMAT,
    #             disabled=not use_star_particles
    #         )
    #         col_dark.number_input(
    #             "Сглаживание тёмной компоненты", 
    #             value=0.004, 
    #             format=NUMBER_FORMAT, 
    #             disabled=not use_dark_particles
    #         )

    #         # положение
    #         with st.expander("Галактика в пространстве"):
    #             st.number_input("Угол наклона плоскости галактики", format=NUMBER_FORMAT, help="Угол в градусах")

    #             col_x, col_y, col_z = st.columns(3)
    #             col_x.number_input("X центра", format=NUMBER_FORMAT)
    #             col_y.number_input("Y центра", format=NUMBER_FORMAT)
    #             col_z.number_input("Z центра", format=NUMBER_FORMAT)
    #             col_x.number_input("X скорость центра", format=NUMBER_FORMAT)
    #             col_y.number_input("Y скорость центра", format=NUMBER_FORMAT)
    #             col_z.number_input("Z скорость центра", format=NUMBER_FORMAT)

    #         # параметры сэмплирования
    #         with st.expander("Cэмплирование"):
    #             use_sampling = st.toggle("Использовать сэмплирование", value=False)
    #             col1, col2 = st.columns(2)
    #             col1.number_input("Доля частиц в расчёте [%]", 0, 100, value=100, disabled=not use_sampling)
    #             col2.number_input("Зерно рандома", step=1, disabled=not use_sampling)

    #         st.write(f"Частиц всего: {count_star_particles + count_dark_particles}")



with st.expander("Новый расчёт"):
    calculation_name = st.text_input("Название расчёта")
    no_calculation_name = (calculation_name is None) or len(calculation_name) == 0
    
    # одна галактика
    with st.expander("Начальные условия (упрощённый режим)", expanded=True):

        col_star, col_dark = st.columns(2)


        col_star.number_input(
            "Масса звёздной компоненты", 
            value=1.0,
            format=NUMBER_FORMAT, 
            help="Безразмерная масса",
            key="mass_star"
        )
        col_dark.number_input(
            "Масса тёмной компоненты", 
            value=1.0, 
            format=NUMBER_FORMAT, 
            help="Безразмерная масса",
            key="mass_dark"
        )


        col_star.number_input(
            "Сглаживание звёздной компоненты", 
            value=0.004, 
            format=NUMBER_FORMAT,
            key="soft_star"
        )
        col_dark.number_input(
            "Сглаживание тёмной компоненты", 
            value=0.004, 
            format=NUMBER_FORMAT,
            key="soft_dark"
        )

        ini_files_raw = os.listdir(ini_dir)
        ini_files = [None]
        for ini_file in ini_files_raw:
            file_name, file_ext = os.path.splitext(ini_file)
            ini_files.append(file_name)

        star_file = col_star.selectbox("Файл звёздной компоненты", options=ini_files, key="ini_file_star")
        dark_file = col_dark.selectbox("Файл тёмной компоненты", options=ini_files, key="ini_file_dark")

        @st.dialog("Новый ini-файл компоненты")
        def new_particles_ini_dialog():
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
                    if particles_ini_name in ini_files:
                        raise FileExistsError("Файл компоненты с данным идентификатором уже добавлен.")
                    
                    dst_path = os.path.join(ini_dir, f"{particles_ini_name}.txt")
                    with open(dst_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.rerun()
                    
                except FileExistsError as ex:
                    st.error(f"Ошибка создания файла компоненты. { ex }")


        if st.button("Импорт файла с частицами", use_container_width=True):
            new_particles_ini_dialog()

    with st.expander("Параметры симуляции", expanded=True):

        time_max = st.number_input(
            "Время симуляции",
            format=NUMBER_FORMAT,
            help="Безразмерное время"
        )
        dt_save = st.number_input(
            "Шаг сохранения",
            format=NUMBER_FORMAT,
            help="Безразмерное время"
        )
        dt_dynamics = st.number_input(
            "Шаг интегрирования",
            format=NUMBER_FORMAT,
            help="Безразмерное время"
        )

    with st.expander("Параметры запуска", expanded=True):
        solvers = FilesystemHandler.scan_for_solvers()
        st.selectbox("Используемый солвер", options=solvers)





    
    create_new_calculation = st.button(
        "Создать расчёт", 
        use_container_width=True,
        disabled=no_calculation_name
    )
    if create_new_calculation:

        try:
            FilesystemHandler.create_new_calculation_directory(PROJECT_NAME, calculation_name)
            CommonNavigation.switch_to_calculation_main(PROJECT_NAME, calculation_name)

        except FileExistsError as ex:
            st.error(f"Ошибка создания расчёта. { ex }")
            




# with st.expander("Расчёт 'Региональная конференция 2026'"):

#     data_general = pd.DataFrame([{
#         "Солвер": "v0.0.1-reg_conf",
#         "Дата последнего расчёта": "2026-07-15"
#     }])
#     st.table(data_general.transpose(), hide_header=True)

#     data_params = pd.DataFrame([{
#             "Время симуляции": 30.000,
#             "Шаг сохранения": 0.1,
#             "Шаг интегрирования": 0.001,
#         }]
#     )
#     st.table(data_params.transpose(), hide_header=True)

#     col1, col2 = st.columns(2)
#     col1.button("Перейти к расчёту", use_container_width=True)
#     col2.button("Создать копию расчёта", use_container_width=True)
