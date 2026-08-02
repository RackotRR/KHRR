import streamlit as st

st.title("KHRR")

if not "project_name" in st.query_params:
    st.error("no project name in query params")
    if (st.button(label="Home", use_container_width=True)):
        st.switch_page("pages/select_project.py")
    st.stop()
PROJECT_NAME = st.query_params["project_name"]

st.header(f"Project '{PROJECT_NAME}'")

with st.expander("Параметры расчёта", expanded=True):
    time_max = st.number_input("Время симуляции [безразмерное время]")
    dt_save = st.number_input("Шаг сохранения [безразмерное время]")
    dt_dynamics = st.number_input("Шаг интегрирования [безразмерное время]")
