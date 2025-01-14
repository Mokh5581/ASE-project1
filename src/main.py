# -----------------------------------------------------------------------------
import os
currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())
import pandas                        as pd
from config                          import pdict
import presentation.streamlit_app as pt
import streamlit as st
import shared.data_processing as m1
import shared.helpers as ht

# -----------------------------------------------------------------------------
@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""
    df_lstat        = pd.read_csv(pdict["file_lstations"], delimiter=";", encoding='utf-8')  # charging stations dataset
    df_geodat_plz   = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")  # Geospatial data for Berlin PLZ
    df_lstat2       = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)  # Preprocessed charging stations
    gdf_lstat3      = m1.count_plz_occurrences(df_lstat2)  # Counts charging stations per PLZ
    df_residents    = pd.read_csv(pdict["file_residents"])  # Population data by PLZ
    gdf_residents2  = m1.preprop_resid(df_residents, df_geodat_plz, pdict)  # Preprocessed population data
    df_reports = pd.read_csv(pdict["file_reports"], delimiter=";", encoding='utf-8')
    df_suggestions = pd.read_csv(pdict["file_suggestions"], delimiter=";", encoding='utf-8')

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
    df_geodat_plz   = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")
    print("Geodata for Berlin loaded.")
    print(df_geodat_plz)
    print(df_lstat.head())
    df_residents    = pd.read_csv(pdict["file_residents"])
    gdf_residents2  = m1.preprop_resid(df_residents, df_geodat_plz, pdict)
    print("Population data processed.")
    print("Streamlit app running.")



if __name__ == "__main__":
    main()
