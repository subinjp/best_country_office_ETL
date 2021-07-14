import pandas as pd
from typing import Tuple,List

class EtlFunctions:
    def __init__(self):
        pass
  
    def reshape_gdp_df(self,gdp_data_df:pd.DataFrame) -> pd.DataFrame:
        
        #print(gdp_data_df)
        gdp_data_df = gdp_data_df.melt(id_vars="Country",
                                var_name="time", 
                                value_name="gdp_value")
        #print(gdp_data_df)
        return gdp_data_df

    def clean_gdp_data(self,gdp_data_df:pd.DataFrame)->Tuple[ List[str], pd.DataFrame]:
       
        office_list = gdp_data_df['Country'].loc[gdp_data_df['gdp_value'].str.contains('Offices|Office', na=False)].to_list()
        gdp_data_df = gdp_data_df.loc[~gdp_data_df['gdp_value'].str.contains('Offices|Office', na=False)]
        subset_cols = ['time','gdp_value']
        gdp_data_df = gdp_data_df.dropna(subset=subset_cols)
        gdp_data_df['gdp_value'] = pd.to_numeric(gdp_data_df['gdp_value'].str.replace(',',''), errors='coerce') 
        #gdp_data_df['gdp_value'] = gdp_data_df.gdp_value.str.replace(',','').astype(float)
        return office_list,gdp_data_df

    def clean_ict_data(self,ict_data_df:pd.DataFrame,office_list:List[str]) -> pd.DataFrame:
       
        # drop rows with missing values -> session_id, page_type, event_type 
        subset_cols = ['geo','time','value']
        ict_data_df = ict_data_df.dropna(subset=subset_cols)
        ict_data_df = ict_data_df[['geo','time','value']].loc[~ict_data_df['geo'].isin(office_list) ]
        ict_data_df = ict_data_df.rename(columns={'geo':'Country','value': 'ict_value'})
        return ict_data_df

    def clean_cloud_service_data(self,cloud_service_data_df:pd.DataFrame,office_list:List[str]) -> pd.DataFrame:
        
        # drop rows with missing values -> session_id, page_type, event_type 
        subset_cols = ['geo','time','value']
        cloud_service_data_df = cloud_service_data_df.dropna(subset=subset_cols)
        #filter out values for large enterprises
        cloud_service_data_df = cloud_service_data_df.loc[cloud_service_data_df['sizen_r2']=='Large enterprises (250 persons employed or more), without financial sector']
        cloud_service_data_df = cloud_service_data_df[['geo','time','value']].loc[~cloud_service_data_df['geo'].isin(office_list)]
        cloud_service_data_df = cloud_service_data_df.rename(columns={'geo':'Country','value':'cloud_value'})
        return cloud_service_data_df
    
    def merge_dataframes(self,ict_data_df:pd.DataFrame,cloud_services_data_df:pd.DataFrame,gdp_data_df:pd.DataFrame)-> pd.DataFrame:
        
        cloud_ict_df = pd.merge(cloud_services_data_df, ict_data_df, how="inner", on=["Country", "time"])
        cloud_ict_gdp_df = pd.merge(cloud_ict_df, gdp_data_df, how="inner", on=["Country","time"])
        cloud_ict_gdp_df['time'] = cloud_ict_gdp_df['time'].astype(int)
        #print(cloud_ict_gdp_df)

        return cloud_ict_gdp_df
        
    def calculate_attractiveness_country(self, cloud_ict_gdp_df:pd.DataFrame)-> pd.DataFrame:
        
        cloud_ict_gdp_df['attractivenes_value']  = cloud_ict_gdp_df[['ict_value','cloud_value','gdp_value']].prod(axis=1).astype(int)
        attractive_country_df = cloud_ict_gdp_df[['Country','time','attractivenes_value']]
        return attractive_country_df
    