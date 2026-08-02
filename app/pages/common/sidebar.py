import streamlit as st

CAN_SWITCH_TO_SELECT_PROJECT = 1
CAN_ADD_SOLVER = 2

def make_sidebar(params : dict = {}):

    # sidebar
    with st.sidebar:

        # Выбор проекта

        can_switch_to_select_project = params.get(CAN_SWITCH_TO_SELECT_PROJECT, True)
        switch_to_select_project = st.button(
            "Выбор проекта", 
            use_container_width=True, 
            disabled=not can_switch_to_select_project
        )
        if switch_to_select_project:
            st.switch_page("pages/select_project.py")


        # Добавление солвера

        can_switch_to_add_solver = params.get(CAN_ADD_SOLVER, True)
        switch_to_add_solver = st.button(
            "Добавить солвер", 
            use_container_width=True,
            disabled=not can_switch_to_add_solver
        )
        if switch_to_add_solver:
            st.switch_page("pages/add_solver.py")