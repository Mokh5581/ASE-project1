# src/presentation/streamlit_app.py
import streamlit as st
from charging.application.services.search_service import SearchService
import folium
from streamlit_folium import st_folium
import pandas as pd

# Initialize search service
# search_service = SearchService()
#
# # Streamlit UI
# st.title("ChargeHub Berlin ⚡")
# postal_code = st.text_input("Enter your postal code:", "")
#
# if postal_code:
#     # Get charging stations by postal code
#     stations = search_service.search_by_postal_code(postal_code)
#     if stations:
#         # Create a map centered on Berlin
#         m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)
#
#         # Add markers to the map
#         for station in stations:
#             color = "green" if station.status == "available" else "red"
#             folium.Marker(
#                 location=station.location,
#                 popup=f"{station.name} ({station.status})",
#                 icon=folium.Icon(color=color)
#             ).add_to(m)
#
#         # Display map in Streamlit
#         st_folium(m, width=700, height=500)
#     else:
#         st.write("No charging stations found for this postal code.")
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
            df_suggestions.to_csv("./charging/infrastructure/repositories/suggestions.csv", sep=";", index=False)
            st.success("Your suggestion has been submitted!")


def render_malfunction_report_page(df_lstat, df_reports):
    st.title("Report Malfunction at Charging Station")
    with st.form("malfunction_report"):
        station_name = st.selectbox("Select Charging Station", df_lstat["Anzeigename (Karte)"].unique())
        report_description = st.text_area("Describe the Malfunction")
        report_location = st.text_input("Address")
        submitted = st.form_submit_button("Submit")
        if submitted:
            new_report = pd.DataFrame({"station_name": [station_name], "report_description": [report_description], "address" : [report_location]})
            df_reports = pd.concat([df_reports, new_report], ignore_index=True)
            df_reports.to_csv("./charging/infrastructure/repositories/malfunction_reports.csv", sep=";", index=False)
            st.success("Your report has been submitted!")



def render_view_suggestions_page(df_suggestions):
    st.title("View Suggestions for New Charging Locations")
    st.dataframe(df_suggestions)

def render_view_malfunction_reports_page(df_reports):
    st.title("View Malfunction Reports")
    st.dataframe(df_reports)