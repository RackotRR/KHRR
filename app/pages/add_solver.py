import streamlit as st
import os
import pages.common.sidebar as CommonSidebar

st.title("KHRR")

st.header("Добавить солвер")

solver_name = st.text_input("Идентификатор (версия) солвера")


CommonSidebar.make_sidebar({ 
    CommonSidebar.CAN_ADD_SOLVER: False
})