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
    # # Read data from csv
    # latency_df = read_data('./csv_results/latency_by_app_custom_shape_20230324121659.csv')

    # #  Plot all MS Latency
    # plot_all_latency(latency_df, ms_names)
    # plot_by_destination(latency_df,"frontend",ms_names)

    # Compare Two Latency
    compare_latencies('./csv_results/latency_by_app_custom_shape_20230324121659.csv',
                      'Configurazione 1',
                      './csv_results/latency_by_app_custom_shape_20230401142549.csv',
                      'Configurazione 2')
    compare_replicas('./csv_results/post_export_1.1_replicas_available_custom_shape_2023-04-03 10_40_16.635271.csv',
                      'Configurazione 1',
                      './csv_results/post_export_1.2_replicas_available_custom_shape_2023-04-03 10_40_16.800430.csv',
                      'Configurazione 2')

if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "loadgenerator", "productcatalogservice", "recommendationservice", "shippingservice", "redis-cart"]

    main(ms_names)
