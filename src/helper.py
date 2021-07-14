import pandas as pd
from pyjstat import pyjstat
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def read_jsonstat_data(url:str)->pd.DataFrame:
    
    try:
        # read from json-stat
        results = pyjstat.Dataset.read(url)
        jsonstat_df = results.write('dataframe')
        return jsonstat_df
    except:
        print(f"Error  in reading jsonstat file {url}")
        sys.exit(1)

def read_gdp_data()->pd.DataFrame:

    try:
        current_working_dir = os.getcwd()
        input_file = os.path.join(current_working_dir, "../data/gdp_data.csv")
        #input_file = '../data/gdp_data.csv'
        gdp_df = pd.read_csv(input_file,sep='|' )
        return gdp_df
    except:
        print("Error  in reading gdp file")
        sys.exit(1)


def averageof_cloudvalues(cloud_services_data_df:pd.DataFrame)->pd.DataFrame:
    cloud_services_data_df = cloud_services_data_df[['geo' ,'time', 'cloud_value']].groupby(['geo','time']).mean().reset_index()
    #print(cloud_services_data_df.loc[cloud_services_data_df['geo']=='Slovakia'])
    return cloud_services_data_df

def visualise_data_over_years(attractve_country_df:pd.DataFrame,output_data:str)->None:
   
    #print(attractve_country_df.sort_values('attractivenes_value',ascending=False))
    number_of_plots = 25
    colormap = plt.cm.nipy_spectral
    plt.rcParams["figure.figsize"] = (22, 10)
    colors = [colormap(i) for i in np.linspace(0, 1,number_of_plots)]
    counties_plot=attractve_country_df.pivot(index='time',columns='Country',values='attractivenes_value')
    counties_plot.plot.bar(title='Attractiveness value of countries over the years',color=colors)
    plt.xlabel("year")
    plt.ylabel("Attractiveness Value")
    plt.ticklabel_format(style='plain', axis='y')
    plt.savefig(output_data+"best_countries_years.png",bbox_inches="tight")

def visualise_data_latest_year(attractve_country_df:pd.DataFrame,output_data:str)->None:
    
    print(attractve_country_df.sort_values('attractivenes_value',ascending=False))
    latest_value_df = attractve_country_df[attractve_country_df.time == attractve_country_df.time.max()].sort_values('attractivenes_value',ascending=False).head(n=5)
    #print(latest_value_df)
    latest_value_df[['Country','attractivenes_value']].set_index('Country').plot(kind='bar',title='Top 5 countries to start office (latest year)')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel("Attractiveness Value")
    plt.savefig(output_data+"top5Countries_latest_yr.png",bbox_inches="tight", dpi=500)
