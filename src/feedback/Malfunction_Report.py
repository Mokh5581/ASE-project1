import streamlit as st
import pandas as pd

class Malfunction_Report:
    def __init__(self, suggestions_df):
        self.suggestions_df = suggestions_df

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