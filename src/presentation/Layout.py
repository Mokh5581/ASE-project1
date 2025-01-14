import streamlit as st
import src.presentation.streamlit_app as pt
import src.shared.data_processing as m1
def navigation_bar_layout(gdf_lstat3,gdf_residents2,df_lstat,df_suggestions,df_reports):
    page = st.sidebar.selectbox("Choose a feature:",
                                ["Home", "Search by Postal Code", "Submit Suggestions", "Report Malfunction",
                                 "View Suggestions", "View Malfunction Reports"])
    if page == "Home":
        # Render home page content
        m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
    elif page == "Search by Postal Code":
        pt.render_search_page(df_lstat)
    elif page == "Submit Suggestions":
        pt.render_submit_suggestion_page(df_suggestions)
    elif page == "Report Malfunction":
        pt.render_malfunction_report_page(df_lstat, df_reports)
    elif page == "View Suggestions":
        pt.render_view_suggestions_page(df_suggestions)
    elif page == "View Malfunction Reports":
        pt.render_view_malfunction_reports_page(df_reports)