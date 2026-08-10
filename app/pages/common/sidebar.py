import streamlit as st
from . import navigation as CommonNavigation

CAN_SWITCH_TO_SELECT_PROJECT = 1
CAN_ADD_SOLVER = 2
CAN_GO_TO_PROJECT_PAGE = 3
HOME_PROJECT = 4

def make_sidebar(params : dict = {}):

    # sidebar
    with st.sidebar:

        # Переход к текущему проекту

        can_go_to_project_page = params.get(CAN_GO_TO_PROJECT_PAGE, False)
        home_project = params.get(HOME_PROJECT, None)
        switch_to_project_page = st.button(
            "Проект",
            use_container_width=True,
            disabled=not can_go_to_project_page or home_project is None
        )
        if switch_to_project_page:
            CommonNavigation.switch_to_project_main(home_project)

        # Выбор проекта

        can_switch_to_select_project = params.get(CAN_SWITCH_TO_SELECT_PROJECT, True)
        switch_to_select_project = st.button(
            "Выбор проекта",
            use_container_width=True,
            disabled=not can_switch_to_select_project
        )
        if switch_to_select_project:
            CommonNavigation.switch_to_select_project()


        # Добавление солвера

        can_switch_to_add_solver = params.get(CAN_ADD_SOLVER, True)
        switch_to_add_solver = st.button(
            "Добавить солвер",
            use_container_width=True,
            disabled=not can_switch_to_add_solver
        )
        if switch_to_add_solver:
            CommonNavigation.switch_to_add_solver()