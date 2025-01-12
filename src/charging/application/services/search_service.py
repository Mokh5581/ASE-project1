# src/charging/application/services/search_service.py
from src.charging.infrastructure.repositories.charging_station_repository import ChargingStationRepository

class SearchService:
    def __init__(self, df_lstat):
        self.df_lstat = df_lstat

    def search_by_postal_code(self, postal_code):
        # Filter dataset for the given postal code

        postal_code = str(postal_code).strip()
        print(f'you are trying to search for : {postal_code}')
        print(f'this is the unfiltered df: {self.df_lstat}')
        print("Unique postal codes in the dataset:", self.df_lstat["Postleitzahl"].unique())

        # Normalize the postal codes in the dataframe
        self.df_lstat["Postleitzahl"] = self.df_lstat["Postleitzahl"].astype(str).str.strip()
        postal_code = str(postal_code).strip()

        filtered_df = self.df_lstat[self.df_lstat["Postleitzahl"] == postal_code]

        stations = []
        print(f'this is the filtered df: {filtered_df}' )
        for _, row in filtered_df.iterrows():
            long = row["Breitengrad"].replace(',','.')
            mag = row["Längengrad"].replace(',','.')
            stations.append({
                "name": row["Anzeigename (Karte)"],
                # "status": row["status"],
                 "location": (float(long), float(mag)),
            })


        return stations
