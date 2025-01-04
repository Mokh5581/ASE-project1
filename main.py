# -----------------------------------------------------------------------------
import os
currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())

import pandas                        as pd
from core import methods             as m1
from core import HelperTools         as ht

from config                          import pdict

# -----------------------------------------------------------------------------
@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""

    df_geodat_plz   = pd.read_csv(pdict["file_geodat_plz"], delimiter=";")  # Geospatial data for Berlin PLZ
    print("Geodata for Berlin loaded.")
    
    df_lstat        = pd.read_csv(pdict["file_lstations"], delimiter=";", encoding='utf-8')  # Charging stations dataset
    print(df_lstat.columns)
    

    df_lstat2       = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)  # Preprocessed charging stations
    gdf_lstat3      = m1.count_plz_occurrences(df_lstat2)  # Counts charging stations per PLZ
    
    df_residents    = pd.read_csv(pdict["file_residents"])  # Population data by PLZ
    gdf_residents2  = m1.preprop_resid(df_residents, df_geodat_plz, pdict)  # Preprocessed population data
    print("Population data processed.")

    # Create Streamlit app for visualization
    m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
    print("Streamlit app running.")
    
# -----------------------------------------------------------------------------------------------------------------------

    #


if __name__ == "__main__": 
    main()

