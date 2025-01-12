# src/presentation/streamlit_app.py
import streamlit as st
from charging.application.services.search_service import SearchService
import folium
from streamlit_folium import st_folium

# Initialize search service
search_service = SearchService()

# Streamlit UI
st.title("ChargeHub Berlin ⚡")
postal_code = st.text_input("Enter your postal code:", "")

if postal_code:
    # Get charging stations by postal code
    stations = search_service.search_by_postal_code(postal_code)
    if stations:
        # Create a map centered on Berlin
        m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)

        # Add markers to the map
        for station in stations:
            color = "green" if station.status == "available" else "red"
            folium.Marker(
                location=station.location,
                popup=f"{station.name} ({station.status})",
                icon=folium.Icon(color=color)
            ).add_to(m)

        # Display map in Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.write("No charging stations found for this postal code.")
