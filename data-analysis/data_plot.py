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

def main(latency_by_app_csv, ms_names):
    # # Read data from csv
    latency_df = read_data(latency_by_app_csv)

    #  Plot all MS Latency
    plot_all_latency(latency_df, ms_names)
    plot_by_destination(latency_df,"frontend",ms_names)

if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "loadgenerator", "productcatalogservice", "recommendationservice", "shippingservice", "redis-cart"]

    main('./csv_results/latency_by_app_custom_shape_20230324121659.csv', ms_names)
