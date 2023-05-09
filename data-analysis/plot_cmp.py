# █▀▄ ▄▀█ ▀█▀ ▄▀█   █▀█ █░░ █▀█ ▀█▀
# █▄▀ █▀█ ░█░ █▀█   █▀▀ █▄▄ █▄█ ░█░

import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from my_modules.plot_latencies import *
from my_modules.data_csv import *

logging.basicConfig(level=logging.INFO)


def main( ms_names):
     # Read data from csv
    # latency_df = read_data('./csv_results/config1/latency_by_app_custom_shape_23042023_144349.csv')
    histogram_data_90 = read_data('./csv_results/config1/histogram_quantile_0_90_23042023_144349.csv')
    cpu_df = read_data('./csv_results/config1/cpu_percentance_by_pod_custom_shape_23042023_144349.csv')
    
    # Filter data based on timestamp
    timestamp = pd.Timestamp('2023-04-23 14:30:49')
    cpu_df = cpu_df[(cpu_df['timestamp'] <= timestamp) & (cpu_df['timestamp'] >= timestamp - pd.Timedelta(minutes=12))]
    histogram_data_90 = histogram_data_90[(histogram_data_90['timestamp'] <= timestamp) & (histogram_data_90['timestamp'] >= timestamp - pd.Timedelta(minutes=12))]
    
    
    # Divide value column by 200 for frontend pod in cpu_df
    ts = cpu_df[cpu_df['pod'].str.contains("frontend")]
    ts['value'] = ts['value'] / 200
    
    # Merge dataframes based on timestamp
    merged_df = pd.merge(ts[['timestamp', 'value']], histogram_data_90[['timestamp', 'value']], on='timestamp')
    
    # Create the plot
    plt.plot(merged_df['value_x'], merged_df['value_y'])
    plt.xlabel('Utilizzo della CPU')
    plt.ylabel('90 percentile')
    plt.show()
    
    

if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"]

    main(ms_names)
