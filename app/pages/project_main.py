import streamlit as st
import pandas as pd
import pages.common.sidebar as CommonSidebar
import pages.common.navigation as CommonNavigation
import pages.common.calc_params as CommonCalcParams
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
calculations = FilesystemHandler.scan_for_calculations(PROJECT_NAME)

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

    st.session_state["ini_params"] = CommonCalcParams.make_ini_params(
        PROJECT_NAME,
        st.session_state.get("ini_params", {})
    )

    st.session_state["sim_params"] = CommonCalcParams.make_sim_params(
        st.session_state.get("sim_params", {})
    )

    CommonCalcParams.make_run_params()

    create_new_calculation = st.button(
        "Создать расчёт",
        use_container_width=True,
        disabled=no_calculation_name
    )
    if create_new_calculation:

        try:
            FilesystemHandler.create_new_calculation_directory(PROJECT_NAME, calculation_name)
            DbHandler.fill_calculation_db(
                PROJECT_NAME,
                calculation_name,
                st.session_state["ini_params"],
                st.session_state["sim_params"])
            CommonNavigation.switch_to_calculation_main(PROJECT_NAME, calculation_name)

        except FileExistsError as ex:
            st.error(f"Ошибка создания расчёта. { ex }")

for calculation in calculations:
    with st.expander(f"Расчёт '{calculation}'"):

        with open("") as f:
            json.

        data_params = pd.DataFrame([{
                "Время симуляции": 30.000,
                "Шаг сохранения": 0.1,
                "Шаг интегрирования": 0.001,
            }]
        )
        st.table(data_params.transpose(), hide_header=True)

        col1, col2 = st.columns(2)
        col1.button("Перейти к расчёту", use_container_width=True)
        col2.button("Создать копию расчёта", use_container_width=True)


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
