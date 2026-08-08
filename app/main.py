import streamlit as st
import utils.db_handler as DbHandler
import pages.common.navigation as CommonNavigation

DbHandler.init_general_db()

page = st.navigation(CommonNavigation.PAGES)
page.run()