import streamlit as st

def make_sidebar(params):

    # sidebar
    with st.sidebar:

        st.button("Выбор проекта", use_container_width=True)

        if st.button("Добавить солвер", use_container_width=True):
            st.switch_page("pages/add_solver.py")