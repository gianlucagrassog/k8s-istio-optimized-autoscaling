import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from my_modules.plot_latencies import *
from my_modules.data_csv import *

logging.basicConfig(level=logging.INFO)

def plot_histogram(*histogram_data, names):
    bins = list(range(0, int(max(d["value"].max() for d in histogram_data)), 100))

    # Create a figure with subplots for each histogram
    fig, axs = plt.subplots( len(histogram_data), 1,figsize=(5, 15))

    # Plot each histogram on its corresponding subplot
    for i, data in enumerate(histogram_data):
        axs[i].hist(data["value"], bins=bins, density=True)
        axs[i].set_title(f"{names[i]} Percentile Distribution")
        axs[i].set_xlabel('Value(ms)')
        axs[i].set_ylabel('Frequency')

    # Display the plot
    plt.show()

def main( ms_names):
    histogram_data_99 = read_data('./csv_results/histogram_quantile_99.csv')
    histogram_data_90 = read_data('./csv_results/histogram_quantile_90.csv')
    histogram_data_50 = read_data('./csv_results/histogram_quantile_50.csv')
    plot_histogram(histogram_data_99,histogram_data_90,histogram_data_50,names=["99th","90th","50th"])
    
    

if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "loadgenerator", "productcatalogservice", "recommendationservice", "shippingservice", "redis-cart"]

    main(ms_names)