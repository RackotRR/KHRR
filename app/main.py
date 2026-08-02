import streamlit as st
import utils.db_handler as DbHandler

DbHandler.init_general_db()

page = st.navigation([
    st.Page("pages/select_project.py", title="Select project"),
    st.Page("pages/set_calc_params.py", title="Set calc params"),
    st.Page("pages/add_solver.py", title="Add solver")
])
page.run()