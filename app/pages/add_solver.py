import streamlit as st
import os
import sys
import pages.common.sidebar as CommonSidebar
import utils.db_handler as DbHandler
import utils.filesystem_handler as FilesystemHandler

st.title("KHRR")

solvers_raw = os.listdir(FilesystemHandler.solvers_dir)
solvers = []
for solver_path in solvers_raw:
    file_name, file_ext = os.path.splitext(solver_path)
    solvers.append(file_name)

with st.container(border=True):

    st.header("Добавить солвер")

    solver_name = st.text_input("Идентификатор (версия) солвера")
    no_solver_name = (solver_name is None) or (len(solver_name) == 0)

    uploaded_file = st.file_uploader("Исполняемый файл солвера", type=["exe", ""])
    no_uploaded_file = (uploaded_file is None) or (uploaded_file is None)

    add_solver = st.button(
        "Добавить",
        use_container_width=True,
        disabled = no_solver_name or no_uploaded_file
    )
    if add_solver:
        file_ext = ".exe" if sys.platform == "win32" else ""
        dst_path = os.path.join(FilesystemHandler.solvers_dir, f"{solver_name}{file_ext}")

        try:
            if solver_name in solvers:
                raise FileExistsError("Солвер с данным идентификатором уже добавлен.")

            # копируем солвер
            with open(dst_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success("Солвер успешно добавлен")
            st.rerun()
        except FileExistsError as ex:
            st.error(ex)
        except Exception as ex:
            # удаляем, что удалось создать
            if (os.path.exists(dst_path)):
                os.remove(dst_path)

            st.error(f"Не удалось добавить солвер: {ex}")



with st.container(border=True):

    st.header("Список солверов")

    st.write(f"Доступно: { len(solvers) } солверов")
    for id, solver_name in enumerate(solvers):
        st.write(f"[{id}] {solver_name}")


CommonSidebar.make_sidebar({ 
    CommonSidebar.CAN_ADD_SOLVER: False
})