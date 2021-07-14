from typing import List,Tuple
import helper
from etl_functions import EtlFunctions
import os
import pandas as pd
#cloud url
cloud_service_url = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/isoc_cicce_use?sizen_r2=M_C10_S951_XK&sizen_r2=L_C10_S951_XK&unit=PC_ENT&indic_is=E_CC"
#ict url 
ict_url =  "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/tin00074?nace_r2=ICT"

#location to store output
current_working_dir = os.getcwd()

output_data = os.path.join(current_working_dir, "../output/")
print(output_data)
def process_gdp_data(etl_functions: EtlFunctions)->Tuple[ List[str], pd.DataFrame]:
    
    gdp_data_df = helper.read_gdp_data()
    new_gdp_data_df = etl_functions.reshape_gdp_df(gdp_data_df)
    office_list, new_gdp_data_df = etl_functions.clean_gdp_data(new_gdp_data_df)
    return office_list, new_gdp_data_df

def process_ict_data(office_list:List[str],etl_functions:EtlFunctions)->pd.DataFrame:
    
    ict_data_df = helper.read_jsonstat_data(ict_url)
    new_ict_data_df = etl_functions.clean_ict_data(ict_data_df,office_list)
    return new_ict_data_df

def process_cloud_services_data(office_list,etl_functions)->pd.DataFrame:
 
    cloud_services_data_df = helper.read_jsonstat_data(cloud_service_url)
    new_cloud_services_data_df = etl_functions.clean_cloud_service_data(cloud_services_data_df,office_list)
    return new_cloud_services_data_df


def main():
    etl_functions = EtlFunctions()

    office_list, gdp_data_df = process_gdp_data(etl_functions)
    ict_data_df = process_ict_data(office_list,etl_functions)
    cloud_services_data_df = process_cloud_services_data(office_list,etl_functions)

    cloud_ict_gdp_df = etl_functions.merge_dataframes(ict_data_df,cloud_services_data_df,gdp_data_df)
    country_attractve_df = etl_functions.calculate_attractiveness_country(cloud_ict_gdp_df)
    
    helper.visualise_data_over_years(country_attractve_df,output_data)
    helper.visualise_data_latest_year(country_attractve_df,output_data)

if __name__ == "__main__":
    main()
