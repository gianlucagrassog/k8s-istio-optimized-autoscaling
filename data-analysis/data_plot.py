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
    # latency_df = read_data('./csv_results/config1/latency_by_app_ramp_23042023_145806.csv')
    # plot_cpu('./csv_results/config1/cpu_percentance_by_pod_custom_shape_23042023_144349.csv', ms_names)
    # #  Plot all MS Latency
 
    # plot_by_destination(latency_df,"frontend",ms_names)

    # # Compare Two Latency config 1 e 2
    # compare_latencies('./csv_results/config1/1/latency_by_app_custom_shape_10052023_084812.csv',
    #                   'Config 1',
    #                   './csv_results/config2/latency_by_app_custom_shape_09052023_203706.csv',
    #                   'Config 2: HPA su frontend', np.arange(5, 1500, 5))
    # Compare Two Latency config 1 e 2
    # compare_latencies('./csv_results/config1/1/latency_by_app_ramp_10052023_085940.csv',
    #                   'Configurazione 1',
    #                   './csv_results/config2/latency_by_app_ramp_09052023_205045.csv',
    #                   'Configurazione 2 con HPA su frontend', np.arange(5, 600, 5))
    
    #### config 1
    # latency_df = read_data('./csv_results/config1/1/latency_by_app_custom_shape_10052023_084812.csv')
    # plot_by_destination(latency_df,"frontend",ms_names,np.arange(5, 1500, 5))     
    # latency_df = read_data('./csv_results/config1/1/latency_by_app_ramp_10052023_085940.csv')
    # plot_by_destination(latency_df,"frontend",ms_names,np.arange(5, 600, 5))    
    # compare_replicas('./csv_results/post_export_1.1_replicas_available_custom_shape_2023-04-03 10_40_16.635271.csv',
    #                   'Configurazione 1',
    #                   './csv_results/post_export_1.2_replicas_available_custom_shape_2023-04-03 10_40_16.800430.csv',
    #                   'Configurazione 2')
     #### config 2
    latency_df = read_data('./csv_results/config2/latency_by_app_custom_shape_09052023_203706.csv')
    plot_all_latency(latency_df, ms_names)
    # plot_by_destination(latency_df,"frontend",ms_names,np.arange(5, 1500, 5))     
    # latency_df = read_data('./csv_results/config2/latency_by_app_ramp_09052023_205045.csv')
    # plot_by_destination(latency_df,"frontend",ms_names,np.arange(5, 600, 5))    

    #### config 3
    latency_df = read_data('./csv_results/config3/3/histogram_quantile_0_50_11052023_090137.csv')
    plot_by_destination(latency_df,"frontend",ms_names,np.arange(10, 1500, 5))     
    latency_df = read_data('./csv_results/config3/3/latency_by_app_ramp_11052023_091446.csv')
    plot_by_destination(latency_df,"frontend",ms_names,np.arange(15, 600, 5))    

if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"]
    # ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
    #             "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice","loadgenerator"]
    main(ms_names)
