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
    plt.legend(fontsize='small')
    plt.show()


def plot_by_destination(latency_df,destination, ms_names,time_range):
    latency_dfs = {}
    for source in ms_names:
        ts = latency_df[(latency_df['source_app'] == source) & (latency_df['destination_app'] == destination)]
        
   
        key = source + '_' + destination
        if not ts.empty:
            print(ts.min())
            print(ts.max())
            print(ts.mean())
            latency_dfs[key] = ts

    for key in latency_dfs:
        df = latency_dfs[key]
        print(df.min())
        print(df.max())
        print(df.mean())
        df = df[:-1]
        source, destination = key.split('_')
        plt.figure(figsize=(6, 5))
        plt.plot(time_range, df['value'], label=f'{source} to {destination}')
    
    
        plt.xlabel('Time (s)')
        plt.ylabel('Latency (ms)')
        plt.legend()
        plt.show()


def compare_latencies(csv_1,sim_name1,csv_2,sim_name2,time_range):

    # Read data from csv
    latency_df_1 = read_data(csv_1)
    latency_df_2 = read_data(csv_2)

    ts1 = latency_df_1[(latency_df_1['source_app'] == 'loadgenerator') & (
        latency_df_1['destination_app'] == 'frontend')]
 
    ts2 = latency_df_2[(latency_df_2['source_app'] == 'loadgenerator') & (
        latency_df_2['destination_app'] == 'frontend')]
    

    # # Drop Rows
    

    
    fig = plt.figure(figsize=(6, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(time_range, ts1['value'], label=f'{sim_name1}')
    ax1.plot(time_range, ts2['value'], label=f'{sim_name2}')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Response Time (ms)')

    # make a legend for both plots
    leg = ax1.legend(loc='upper left')
    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    plt.show()

def filter_data_replicas(df):
    return df[(df['deployment'] == 'frontend')]

def compare_replicas(csv_1,sim_name1,csv_2,sim_name2,time_range):

    # Read data from csv
    replicas_df_1 = read_data(csv_1)
    replicas_df_2 = read_data(csv_2)

    replicas_1 = filter_data_replicas(replicas_df_1)
    replicas_2 = filter_data_replicas(replicas_df_2)
    
    # Drop Rows
    replicas_1= replicas_1[:-3]
    replicas_2= replicas_2[:-3]


    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)

    ax1.plot(time_range, replicas_1['value'],  label=f'RT 1:{sim_name1}')
    ax1.plot(time_range, replicas_2['value'],  label=f'RT 2:{sim_name2}')
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel('Available Replicas frontend (num)')
    leg = ax1.legend()
    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    plt.show()
def plot_cpu(csv_1,ms_names):

    cpu_df=read_data(csv_1)
    cpu_dfs = {}

    for ms_name in ms_names:
     
        ts = cpu_df[cpu_df['pod'].str.contains(ms_name)]
        if not ts.empty:
            cpu_dfs[ms_name] = ts
            cpu_dfs[ms_name]['value']=(cpu_dfs[ms_name]['value']/200)
            print(f"{ms_name} min:{ts['value'].min()}")
            print(f"{ms_name} max:{ts['value'].max()}")
            print(f"{ms_name} avg:{ts['value'].mean()}")

    for key in cpu_dfs:
        df = cpu_dfs[key]
        plt.plot(df['timestamp'], df['value'], label=f'{key}')

    leg = plt.legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(1.0)
    plt.ylabel('CPU Cores')
    plt.xlabel('Time(s)')
    plt.legend()
    plt.show()
