import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from my_modules.data_csv import *


def plot_all_latency(latency_df,ms_names):
    latency_dfs = {}

    for source in ms_names:
        for destination in ms_names:
            print(source+" to "+destination)
            ts = latency_df[(latency_df['source_app'] == source) & (
                latency_df['destination_app'] == destination)]
            print(ts)
            key = source + '_' + destination
            if not ts.empty:
                latency_dfs[key] = ts

    for key in latency_dfs:
        df = latency_dfs[key]
        source, destination = key.split('_')
        plt.plot(df['timestamp'], df['value'], label=f'{source} to {destination}')

    plt.xlabel('timestamp')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.show()


def plot_by_destination(latency_df,destination, ms_names):
    latency_dfs = {}

    for source in ms_names:
        print(source+" to "+destination)
        ts = latency_df[(latency_df['source_app'] == source) & (
            latency_df['destination_app'] == destination)]
        print(ts)
        key = source + '_' + destination
        if not ts.empty:
            latency_dfs[key] = ts

    for key in latency_dfs:
        df = latency_dfs[key]
        source, destination = key.split('_')
        plt.plot(df['timestamp'], df['value'], label=f'{source} to {destination}')

    plt.xlabel('Timestamp')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.show()


def compare_latencies(csv_1,sim_name1,csv_2,sim_name2):

    # Read data from csv
    latency_df_1 = read_data(csv_1)
    latency_df_2 = read_data(csv_2)

    ts1 = latency_df_1[(latency_df_1['source_app'] == 'loadgenerator') & (
        latency_df_1['destination_app'] == 'frontend')]
 
    ts2 = latency_df_2[(latency_df_2['source_app'] == 'loadgenerator') & (
        latency_df_2['destination_app'] == 'frontend')]
    # Drop Rows
    ts1 = ts1[:-1]

    time_range = np.arange(5, 1200, 5)

    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)
    ax1.plot(time_range, ts1['value'], label=f'RT 1:{sim_name1}')
    ax1.plot(time_range, ts2['value'], label=f'RT 2:{sim_name2}')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Response Time (ms)')

    # make a legend for both plots
    leg = ax1.legend()
    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    plt.show()


# def plot_cpu(cpu_df):

#     cpu_dfs = {}

#     for i in range(len(ms_names)):
    
#         ms_name = ms_names[i]
#         ts = cpu_df[cpu_df['pod'].str.contains(ms_name)]
#         print(ts)
#         if not ts.empty:
#             cpu_dfs[key] = ts

#     for key in cpu_dfs:
#         df = cpu_dfs[key]
#         plt.plot(df['timestamp'], df['value'], label=f'{key}')

#     plt.ylabel('CPU Percentage (%)')
#     plt.xlabel('Users (num)')
#     plt.legend()
#     plt.show()
