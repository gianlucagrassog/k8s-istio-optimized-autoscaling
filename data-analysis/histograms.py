import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from my_modules.plot_latencies import *
from my_modules.data_csv import *
import random
logging.basicConfig(level=logging.INFO)

def plot_histogram(*histogram_data, names):
    bins = list(range(0, int(max(d["value"].max() for d in histogram_data)), 100))

    # Create a figure with subplots for each histogram
    fig, axs = plt.subplots(1 ,len(histogram_data) ,figsize=(12.8, 4.8))
    # fig.subplots_adjust(hspace=0.4,left=0.16)

    # Plot each histogram on its corresponding subplot
    for i, data in enumerate(histogram_data):
        axs[i].hist(data["value"], bins=bins, density=True)
        axs[i].set_title(f"{names[i]} Percentile Distribution")
        axs[i].set_xlabel('Value(ms)')
        axs[i].set_ylabel('Frequency')

    # Display the plot
    plt.show()

def compare_two_histograms(*histogram_data, names,percentile):
    x = [histogram_data[0]["value"]]
    y = [histogram_data[1]["value"]]

    bins = list(range(0, int(max(d["value"].max() for d in histogram_data)), 100))
    plt.title(f"{percentile}th Percentile Distribution")
    plt.hist(x, bins,density=True, label=f'{names[0]}')
    plt.hist(y, density=True, label=f'{names[1]}')
    plt.xlabel('Value(ms)')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()

def main():

    # # # Configuration 1 
    # histogram_data_99 = read_data('./csv_results/config1/1/histogram_quantile_0_99_10052023_084812.csv')
   # histogram_data_90 = read_data('./csv_results/config1/1/histogram_quantile_0_90_10052023_084812.csv')
    # histogram_data_50 = read_data('./csv_results/config1/1/histogram_quantile_0_50_10052023_084812.csv')
    # # # plot_histogram(histogram_data_99,histogram_data_90,histogram_data_50,names=["99th","90th","50th"])
    # plot_histogram(histogram_data_99,histogram_data_90,names=["99th","90th"])
    histogram_data_90 = read_data('./csv_results/config2/histogram_quantile_0_50_09052023_203706.csv')
    histogram_data_50 = read_data('./csv_results/config2/histogram_quantile_0_50_09052023_203706.csv')
    plot_histogram(histogram_data_50,histogram_data_90,names=["50th","90th"])
    
    compare_two_histograms(read_data('./csv_results/config1/1/histogram_quantile_0_99_10052023_084812.csv')
                           , read_data('./csv_results/config2/histogram_quantile_0_99_09052023_203706.csv')
                           ,names=["Configurazione 1","Configurazione 2: HPA su frontend"]
                           ,percentile="99")
    compare_two_histograms(read_data('./csv_results/config1/1/histogram_quantile_0_90_10052023_084812.csv')
                           , read_data('./csv_results/config2/histogram_quantile_0_90_09052023_203706.csv')
                           ,names=["Configurazione 1","Configurazione 2: HPA su frontend"]
                           ,percentile="90")
    compare_two_histograms(read_data('./csv_results/config1/1/histogram_quantile_0_50_10052023_084812.csv')
                           , read_data('./csv_results/config2/histogram_quantile_0_50_09052023_203706.csv')
                           ,names=["Configurazione 1","Configurazione 2: HPA su frontend"]
                           ,percentile="50")

    # # Configuration 3 
    # histogram_data_99 = read_data('./csv_results/config3/3/histogram_quantile_0_99_11052023_090137.csv')
    # histogram_data_90 = read_data('./csv_results/config3/3/histogram_quantile_0_90_11052023_090137.csv')
    # histogram_data_50 = read_data('./csv_results/config3/3/histogram_quantile_0_50_11052023_090137.csv')

    # # # plot_histogram(histogram_data_99,histogram_data_90,histogram_data_50,names=["99th","90th","50th"])
    # plot_histogram(histogram_data_99,histogram_data_90,names=["99th","90th"])
    # plot_histogram(histogram_data_99,histogram_data_50,names=["99th","50th"])
    # compare_two_histograms(read_data('./csv_results/config1/1/histogram_quantile_0_90_10052023_084812.csv')
    #                        , read_data('./csv_results/config3/3/histogram_quantile_0_90_11052023_090137.csv')
    #                        ,names=["Configurazione Iniziale","Configurazione con Autoscaling"]
    #                        ,percentile="90")
    # compare_two_histograms(read_data('./csv_results/config1/1/histogram_quantile_0_99_10052023_084812.csv')
    #                        , read_data('./csv_results/config3/3/histogram_quantile_0_99_11052023_090137.csv')
    #                        ,names=["Configurazione Iniziale","Configurazione con Autoscaling"]
    #                        ,percentile="99")



    # histogram_data_99 = read_data('./csv_results/config3/histogram_quantile_0_99_24042023_103404.csv')
    # histogram_data_90 = read_data('./csv_results/config3/histogram_quantile_0_90_24042023_103404.csv')
    # histogram_data_50 = read_data('./csv_results/config3/histogram_quantile_0_50_24042023_103404.csv')
    # # plot_histogram(histogram_data_99,histogram_data_90,histogram_data_50,names=["99th","90th","50th"])
    # plot_histogram(histogram_data_99,histogram_data_90,names=["99th","90th"])

    # histogram_data_99_1 = read_data('./csv_results/config1/histogram_quantile_0_99_23042023_144349.csv')
    # histogram_data_99_2 = read_data('./csv_results/config3/histogram_quantile_0_99_24042023_103404.csv')

    # compare_two_histograms(histogram_data_99_1, histogram_data_99_2,names=["Configurazione Iniziale","Configurazione con Autoscaling"])
    # histogram_data_50_1 = read_data('./csv_results/config1/histogram_quantile_0_50_23042023_144349.csv')
    # histogram_data_50_2 = read_data('./csv_results/config3/histogram_quantile_0_50_24042023_103404.csv')

    # compare_two_histograms(histogram_data_50_1, histogram_data_50_2,names=["Configurazione Iniziale","Configurazione con Autoscaling"])

if __name__ == '__main__':
    main()