import streamlit as st
import pages.common.sidebar as CommonSidebar
import utils.db_handler as DbHandler
import utils.filesystem_handler as FilesystemHandler
import os

st.title("KHRR")

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

CommonSidebar.make_sidebar()