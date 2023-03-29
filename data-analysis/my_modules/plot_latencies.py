import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime


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
