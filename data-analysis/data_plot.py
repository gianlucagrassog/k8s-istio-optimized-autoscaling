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



def plot_histogram(histogram_data1,name1,histogram_data2,name2,histogram_data3,name3):
    values1 = histogram_data1["value"]
    values2 = histogram_data2["value"]
    values3 = histogram_data3["value"]


    bins = list(range(0,int(values1.max()),100))

    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    # Plot the histograms on each subplot
    axs[0].hist(values1, bins=bins,density=True)
    axs[1].hist(values2, bins=bins,density=True)
    axs[2].hist(values3, bins=bins,density=True)


    # Set the title and axis labels for each subplot
    axs[0].set_title(f"{name1} Percentile Distribution")
    axs[0].set_xlabel('Value')
    axs[0].set_ylabel('Frequency')

    axs[1].set_title(f"{name2} Percentile Distribution")
    axs[1].set_xlabel('Value(ms)')
    axs[1].set_ylabel('Frequency')
    
    axs[2].set_title(f"{name3} Percentile Distribution")
    axs[2].set_xlabel('Value(ms)')
    axs[2].set_ylabel('Frequency')

    # Display the plot
    plt.show()

def main( ms_names):
    # # Read data from csv
    # latency_df = read_data('./csv_results/latency_by_app_ramp_20230324114317.csv')
    # # plot_cpu('./csv_results/cpu_percentance_by_pod_custom_shape_20230324121659.csv', ms_names)
    # #  Plot all MS Latency
    # # plot_all_latency(latency_df, ms_names)
    # plot_by_destination(latency_df,"frontend",ms_names)

    # # Compare Two Latency
    # compare_latencies('./csv_results/latency_by_app_custom_shape_20230324121659.csv',
    #                   'Configurazione 1',
    #                   './csv_results/latency_by_app_custom_shape_20230401142549.csv',
    #                   'Configurazione 2')
    # compare_replicas('./csv_results/post_export_1.1_replicas_available_custom_shape_2023-04-03 10_40_16.635271.csv',
    #                   'Configurazione 1',
    #                   './csv_results/post_export_1.2_replicas_available_custom_shape_2023-04-03 10_40_16.800430.csv',
    #                   'Configurazione 2')

    histogram_data_99 = read_data('./csv_results/histogram_quantile_99.csv')
    histogram_data_90 = read_data('./csv_results/histogram_quantile_90.csv')
    histogram_data_50 = read_data('./csv_results/histogram_quantile_50.csv')
    plot_histogram(histogram_data_99,"99th",histogram_data_90,"90th",histogram_data_50,"50th")
    
    

if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "loadgenerator", "productcatalogservice", "recommendationservice", "shippingservice", "redis-cart"]

    main(ms_names)
