# src/charging/infrastructure/services/suggestion_service.py
import pandas as pd
import streamlit as st


class SuggestionService:
    def __init__(self, suggestions_df):
        self.suggestions_df = suggestions_df

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