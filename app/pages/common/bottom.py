import streamlit as st

@st.fragment(run_every="15s")
def make_journal(project : str = None, calculation : str = None):

    # нужно читать две БД:
    # - БД приложения с логом приложения (очищается ко кнопке или по лимиту сообщений)
    # - БД расчёта с логом расчёта (очищается при запуске расчёта)

    with st.bottom:
        with st.expander("Журнал"):

            message = ""
            for i in range(0, 100):
                message += f"[20:27] [Debug] Happened thing {i}\n"
            st.text_area("Журнал", message, height=300, label_visibility="collapsed")

            if st.button("Очистить журнал приложения", use_container_width=True):
                st.error("Not implemented")