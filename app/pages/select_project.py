import streamlit as st
import os
import pages.common.sidebar as CommonSidebar
import pages.common.navigation as CommonNavigation
import pages.common.bottom as CommonBottom
import utils.filesystem_handler as FilesystemHandler

st.title("RRGalax[S]im")

# Открытие существующего проекта

with st.container(border=True):

    st.header("Выбор проекта")

    def file_selector():
        filenames = os.listdir(FilesystemHandler.projects_dir)
        selected_filename = st.selectbox(
            "Выберите проект",
            filenames
        )
        return selected_filename

    filename = file_selector()
    switch_to_project = st.button(
        "Открыть",
        use_container_width=True,
        disabled=filename is None
    )
    if switch_to_project:
        CommonNavigation.switch_to_project_main(project_name=filename)

# Создание нового проекта

@st.dialog("Новый проект")
def new_project_dialog():
    new_project_name = st.text_input("Название нового проекта")

    create_new_project = st.button(
        "Создать",
        use_container_width=True,
        disabled=len(new_project_name) == 0
    )
    if create_new_project:
        try:
            FilesystemHandler.create_new_project_directory(new_project_name)
            CommonNavigation.switch_to_project_main(project_name=new_project_name)
        except FileExistsError as ex:
            st.error(f"Ошибка создания проекта. { ex }")



if st.button("Новый проект", use_container_width=True):
    new_project_dialog()

CommonSidebar.make_sidebar({
    CommonSidebar.CAN_SWITCH_TO_SELECT_PROJECT: False
})

CommonBottom.make_journal()