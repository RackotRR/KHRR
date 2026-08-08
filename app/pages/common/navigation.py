import streamlit as st

PAGES = [
    # start page
    st.Page("pages/select_project.py", title="Select project"),
    # other pages
    st.Page("pages/project_main.py", title="Project"),
    st.Page("pages/calculation_main.py", title="Calculation"),
    st.Page("pages/add_solver.py", title="Add solver")
]
    
def switch_to_select_project():
    st.switch_page(
        "pages/select_project.py"
    )

def switch_to_add_solver():
    st.switch_page(
        "pages/add_solver.py"
    )

def switch_to_project_main(project_name : str):
    params = {
        "project_name": project_name 
    }

    st.switch_page(
        "pages/project_main.py", 
        query_params=params
    )

def switch_to_calculation_main(project_name : str, calculation_name : str):
    params = {
        "project_name": project_name,
        "calculation_name": calculation_name
    }

    st.switch_page(
        "pages/calculation_main.py",
        query_params=params
    )