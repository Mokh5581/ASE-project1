# -----------------------------------------------------------------------------
import os

import src.presentation.Layout

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

    src.presentation.Layout.navigation_bar_layout(gdf_lstat3, gdf_residents2, df_lstat, df_suggestions, df_reports)




if __name__ == "__main__":
    main()
