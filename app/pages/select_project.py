import streamlit as st
import os
import pages.common.sidebar as CommonSidebar


st.title("KHRR")

with st.container(border=True):

    st.header("Выбор проекта")

    def file_selector(folder_path='.'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox('Select a file', filenames)
        return os.path.join(folder_path, selected_filename)

    filename = file_selector()
    st.write('You selected `%s`' % filename)



@st.dialog("Новый проект")
def new_project_dialog():
    new_project_name = st.text_input("Название нового проекта")
    if st.button("Создать"):
        # переходим на страницу с указанным проектом
        st.switch_page("pages/set_calc_params.py", query_params={ "project_name": new_project_name })
    if st.button("Отмена"):
        pass

if st.button("Новый проект", use_container_width=True):
    new_project_dialog()

sidebar = CommonSidebar.make_sidebar()
sidebar["select_project_button"].disabled = True