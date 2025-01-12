# -----------------------------------------------------------------------------
import os
currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())

import pandas                        as pd
# from core import methods             as m1
# from core import HelperTools         as ht

from config                          import pdict
# import os
# import pandas as pd
from charging.application.services.search_service import SearchService
import streamlit as st
import folium
from streamlit_folium import st_folium
# from src.config import pdict
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

    try:
        df_suggestions = pd.read_csv("./community/suggestions.csv", delimiter=";", encoding='utf-8')
    except FileNotFoundError:
        df_suggestions = pd.DataFrame(columns=["postal_code", "address", "comments"])
        df_suggestions.to_csv("./community/suggestions.csv", sep=";", index=False)

    try:
        df_reports = pd.read_csv("./feedback/malfunction_reports.csv", delimiter=";", encoding='utf-8')
    except FileNotFoundError:
        df_reports = pd.DataFrame(columns=["station_name", "report_description"])
        df_reports.to_csv("./feedback/malfunction_reports.csv", sep=";", index=False)
    # page = st.sidebar.selectbox("Choose a feature:", ["Home", "Search by Postal Code"])
    page = st.sidebar.selectbox("Choose a feature:",
                                ["Home", "Search by Postal Code", "Submit Suggestions", "Report Malfunction",
                                 "View Suggestions", "View Malfunction Reports"])
    # print(f'this is the column names {df_lstat2.columns}')

    if page == "Home":
        # Render home page content
        m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
    elif page == "Search by Postal Code":
        render_search_page(df_lstat)
    elif page == "Submit Suggestions":
        render_submit_suggestion_page(df_suggestions)
    elif page == "Report Malfunction":
        render_malfunction_report_page(df_lstat, df_reports)
    elif page == "View Suggestions":
        render_view_suggestions_page(df_suggestions)
    elif page == "View Malfunction Reports":
        render_view_malfunction_reports_page(df_reports)
    df_geodat_plz   = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")  # Geospatial data for Berlin PLZ
    print("Geodata for Berlin loaded.")
    print(df_geodat_plz)
    # st.write("Sample of charging stations data:")
    # st.write(df_lstat.head())

    # st.write("Unique postal codes in the dataset:")
    # st.write(df_lstat["Postleitzahl"].unique())  # Replace `postal_code` with the correct column name

    print(df_lstat.head())
    df_residents    = pd.read_csv(pdict["file_residents"])  # Population data by PLZ
    gdf_residents2  = m1.preprop_resid(df_residents, df_geodat_plz, pdict)  # Preprocessed population data
    print("Population data processed.")

    # Create Streamlit app for visualization
    # m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
    print("Streamlit app running.")

def render_search_page(df_lstat):
    """Render the Search by Postal Code page."""
    search_service = SearchService(df_lstat)  # Initialize SearchService with data
    postal_code = st.text_input("Enter your postal code :", "")
    if postal_code:
        st.write(f"Searching for postal code: {postal_code}")
        stations = search_service.search_by_postal_code(postal_code)
        st.write(f"those are the stations in postal code :{postal_code}")
        st.write(pd.DataFrame(stations))
        print("station are as follow" )
        print(stations)
        # st.write("Debug - Stations Data:", stations)   # Debug output
        if stations:
            m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)
            for station in stations:
                folium.Marker(
                    location=station["location"],
              #      popup=f"{station['name']} ({station['status']})",
                    popup=f"{station['name']} Is ready for you)",
                    # icon=folium.Icon(color="green" if station["status"] == "available" else "red"),
                ).add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.warning("No charging stations found for this postal code.")

def render_submit_suggestion_page(df_suggestions):
    st.title("Submit Suggestion for New Charging Location")
    with st.form("suggestion_form"):
        postal_code = st.text_input("Postal Code")
        address = st.text_input("Address")
        comments = st.text_area("Comments")
        submitted = st.form_submit_button("Submit")
        if submitted:
            new_suggestion = pd.DataFrame([{"postal_code": postal_code, "address": address, "comments": comments}])
            df_suggestions = pd.concat([df_suggestions, new_suggestion], ignore_index=True)
            df_suggestions.to_csv("./community/suggestions.csv", sep=";", index=False)
            st.success("Your suggestion has been submitted!")
            # new_suggestion = {"postal_code": postal_code, "address": address, "comments": comments}
            # df_suggestions = df_suggestions.ap(new_suggestion, ignore_index=True)
            # df_suggestions.to_csv("suggestions.csv", sep=";", index=False)
            # st.success("Your suggestion has been submitted!")

def render_malfunction_report_page(df_lstat, df_reports):
    st.title("Report Malfunction at Charging Station")
    with st.form("malfunction_report"):
        station_name = st.selectbox("Select Charging Station", df_lstat["Anzeigename (Karte)"].unique())
        report_description = st.text_area("Describe the Malfunction")
        submitted = st.form_submit_button("Submit")
        if submitted:
            new_report = pd.DataFrame({"station_name": [station_name], "report_description": [report_description]})
            df_reports = pd.concat([df_reports, new_report], ignore_index=True)
            df_reports.to_csv("./feedback/malfunction_reports.csv", sep=";", index=False)
            st.success("Your report has been submitted!")
            # new_report = {"station_name": station_name, "report_description": report_description}
            # df_reports = df_reports.append(new_report, ignore_index=True)
            # df_reports.to_csv("malfunction_reports.csv", sep=";", index=False)
            # st.success("Your report has been submitted!")


def render_view_suggestions_page(df_suggestions):
    st.title("View Suggestions for New Charging Locations")
    st.dataframe(df_suggestions)

def render_view_malfunction_reports_page(df_reports):
    st.title("View Malfunction Reports")
    st.dataframe(df_reports)
# -----------------------------------------------------------------------------------------------------------------------

    #


if __name__ == "__main__":
    main()

# import os
# import pandas as pd
# from charging.application.services.search_service import SearchService
# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from src.config import pdict
# import shared.data_processing as dp
# import shared.helpers as ht
#
# def main():
#     """Main: Streamlit App for visualizing charging stations and providing search functionality."""
#     st.title("ChargeHub Berlin ⚡")
#     st.sidebar.header("Navigation")
#
#     # Navigation menu
#     page = st.sidebar.selectbox("Choose a feature:", ["Home", "Search by Postal Code"])
#
#     # Load datasets
#     try:
#         df_geodat_plz = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")
#         df_lstat = pd.read_csv(pdict["file_lstations"], delimiter=";", encoding="utf-8")
#         df_residents = pd.read_csv(pdict["file_residents"])
#     except FileNotFoundError as e:
#         st.error(f"File not found: {e.filename}")
#         return
#
#     # Preprocess data
#     df_lstat2 = dp.preprop_lstat(df_lstat, df_geodat_plz, pdict)
#     gdf_lstat3 = dp.count_plz_occurrences(df_lstat2)
#     gdf_residents2 = dp.preprop_resid(df_residents, df_geodat_plz, pdict)
#
#     if page == "Home":
#         st.write("Welcome to ChargeHub Berlin! Use the sidebar to navigate to the features.")
#     elif page == "Search by Postal Code":
#         render_search_page()
#
# def render_search_page():
#     """Render the Search by Postal Code page."""
#     search_service = SearchService()
#     postal_code = st.text_input("Enter your postal code:", "")
#     if postal_code:
#         stations = search_service.search_by_postal_code(postal_code)
#         if stations:
#             m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)
#             for station in stations:
#                 folium.Marker(
#                     location=station.location,
#                     popup=f"{station.name} ({station.status})",
#                     icon=folium.Icon(color="green" if station.status == "available" else "red"),
#                 ).add_to(m)
#             st_folium(m, width=700, height=500)
#         else:
#             st.write("No charging stations found for this postal code.")
#
# if __name__ == "__main__":
#     main()
