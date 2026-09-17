import streamlit as st
import pages.common.sidebar as CommonSidebar
import pages.common.calc_params as CommonCalcParams
import utils.db_handler as DbHandler
import utils.filesystem_handler as FilesystemHandler
import os

st.title("RRGalax[S]im")

if not "project_name" in st.query_params:
    st.error("В параметрах запроса не указано название проекта.")
    if (st.button(label="Home", use_container_width=True)):
        st.switch_page("pages/select_project.py")
    st.stop()
PROJECT_NAME = st.query_params["project_name"]

if not "calculation_name" in st.query_params:
    st.error("В параметрах запроса не указано название расчёта.")
    if (st.button(label="Home", use_container_width=True)):
        st.switch_page("pages/project_main.py")
    st.stop()
CALCULATION_NAME = st.query_params["calculation_name"]

st.header(f"Расчёт '{PROJECT_NAME} : {CALCULATION_NAME}'")

CommonSidebar.make_sidebar({
    CommonSidebar.CAN_GO_TO_PROJECT_PAGE: True,
    CommonSidebar.HOME_PROJECT: PROJECT_NAME
})

st.session_state["calc_params"] = CommonCalcParams.make_params_input(PROJECT_NAME, CALCULATION_NAME)

CommonCalcParams.make_run_params()

if st.button("Сохранить", use_container_width=True):
    DbHandler.fill_calculation_db(
        PROJECT_NAME,
        CALCULATION_NAME,
        st.session_state["calc_params"]
    )
st.button("Запустить расчёт", use_container_width=True)
