import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def read_data(filename):
    try:
        df = pd.read_csv(filename, header=0)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")


# Plot latency curve and returns the timestamp of the intersection between the latency curve and the SLO line.
def plot_latency(latency_df):
    ts1 = latency_df[(latency_df['source_app'] == 'loadgenerator') & (
        latency_df['destination_app'] == 'frontend')]
    ts1 = ts1[ts1['timestamp'] <= pd.Timestamp('2023-03-04 14:36:35')]
    plt.plot(ts1['users'], ts1['value'], label='Loadgenerator to Frontend')
    
    sloy = 1000 * np.ones(len(ts1.index))
    slox = np.arange(5, ts1['users'].tail(1).iloc[0]+5, 5)

    plt.plot(slox, sloy, label='SLO')

    idx = np.argwhere(np.diff(np.sign(sloy - ts1['value']))).flatten()
    
    if idx[0] != 0:
        print(idx[0])
        intersection_point = ts1['users'].iloc[idx[0]]
        plt.plot(ts1['users'].iloc[idx[0]], sloy[idx[0]],
             'ro', label=f'Users = {intersection_point }')
    else:
        intersection_point = ts1['users'].iloc[idx[1]]
        plt.plot(ts1['users'].iloc[idx[1]], sloy[idx[1]],
             'ro', label=f'Users = {intersection_point }')
    
    plt.xlabel('Users (num)')
    plt.ylabel('Response Time (ms)')
    plt.legend()
    plt.show()
    if idx[0] != 0:
        return ts1['timestamp'].iloc[idx[0]]
    else:
        return ts1['timestamp'].iloc[idx[1]]


def plot_cpu(intersection_time, cpu_df):
    pods = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
            "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart"]
    cpu_ts = {}

    for pod in pods:
        ts = cpu_df[cpu_df['pod'].str.contains(pod)]
        ts = ts[ts['timestamp'] == pd.Timestamp(
            intersection_time)]
        # keep the row with the largest value
        if len(ts) > 1:
            ts = ts.nlargest(1, 'value') 
        cpu_ts[pod] = ts
        cpu_ts[pod]['value'].values[0]=(cpu_ts[pod]['value'].values[0]/200)
    
    cpu_ts['recommendationservice']['value'].values[0]=cpu_ts['recommendationservice']['value'].values[0]*2
    cpu_ts['checkoutservice']['value'].values[0]=cpu_ts['checkoutservice']['value'].values[0]*4

    # Sort
    sorted_cpu_ts = sorted(
        cpu_ts.items(), key=lambda x: x[1]['value'].values[0], reverse=True)
    cpu_ts_ordered = {k: v for k, v in sorted_cpu_ts}

    # Plot cpu_ts using a bar plot
    fig, ax = plt.subplots(figsize=(15, 40))
    values = [ts['value'].values[0] for ts in cpu_ts_ordered.values()]
    labels = cpu_ts_ordered.keys()

    sns.barplot(x=list(labels), y=values,  palette="Blues_r", ax=ax)
    ax.set_ylabel('CPU Percentage')
    ax.set_xlabel('Pod')
    ax.set_title('CPU Usage by Pod')
    ax.xaxis.get_ticklabels()[0].set_weight('bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    #ax.xaxis.get_ticklabels()[0].set_fontsize(12)
    start, end = ax.get_ylim()
    ax.set_yticks(np.arange(start, end+10, 10))
    ax.set_yticks(ax.get_yticks()[::1])
    plt.show()

def plot_all_latency(latency_df):
    pods = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
            "paymentservice","loadgenerator", "productcatalogservice", "recommendationservice", "redis-cart"]
    latency_dfs = {}

    for i in range(len(pods)):
        for j in range(i+1, len(pods)):
            source = pods[i]
            destination = pods[j]
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
        # sns.set_theme(style="white")
        # sns.lineplot(x=df['users'],y=df['value'], label=f'{source} to {destination}')
        plt.plot(df['users'], df['value'], label=f'{source} to {destination}')

    plt.xlabel('Users')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.show()
def plot_by_destination(latency_df,destination):
    pods = [ "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
            "paymentservice", "frontend","productcatalogservice", "recommendationservice", "redis-cart", "loadgenerator"]
    latency_dfs = {}

    for i in range(len(pods)):
        source = pods[i]
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
        # sns.set_theme(style="white")
        # sns.lineplot(x=df['users'],y=df['value'], label=f'{source} to {destination}')
        plt.plot(df['users'], df['value'], label=f'{source} to {destination}')

    plt.xlabel('Users')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.show()
def plot_cpu_80(cpu_df):
    ts = cpu_df[cpu_df['pod'].str.contains('frontend')]
    for index, row in ts.iterrows():
        if(row['value']> 80):
            return row['timestamp']
        
def plot_cpu_frontend(cpu_df):
    ts = cpu_df[cpu_df['pod'].str.contains('frontend')]
   
    plt.plot(ts['users'], ts['value'], label=f'Frontend ms CPU usage')
    
    plt.axvline(x = 135, color="orange",label = 'First autoscaling event: 135 Users')
    plt.axvline(x = 260, color="red",label = 'SLO reached: 260 Users')

    plt.ylabel('CPU Percentage (%)')
    plt.xlabel('Users (num)')
    plt.legend()
    plt.show()

def main(latency_by_app_csv, cpu_percentance_csv):
    # Read data from csv
    latency_df = read_data(latency_by_app_csv)
    cpu_df = read_data(cpu_percentance_csv)

    # # Plot Latency LG -> FE
    # intersection_time = plot_latency(latency_df)

    # # Plot Cpu Usage by Pod
    # plot_cpu(intersection_time,cpu_df)

    # # Plot all MS Latency 
    # plot_all_latency(latency_df)
    # plot_by_destination(latency_df,"frontend")
    timestamp = plot_cpu_80(cpu_df)
    print(timestamp)
    ts = latency_df[latency_df['timestamp'] == pd.Timestamp(timestamp)]
    print(ts['users'])
    
    plot_cpu_frontend(cpu_df)
    # plot_by_destination(latency_df,"currencyservice")
    # plot_by_destination(latency_df,"productcatalogservice")
    

if __name__ == '__main__':


    # #  Configurazione 1 
    main('1_latency_by_app_30s_300_2023-03-01 19:53:34.csv','1_cpu_percentance_by_pod_300_2023-03-01 19:53:34.csv')
    
    # #  Configurazione 2
    # main('2_latency_by_app_30s_300_2023-03-01 20:42:30.csv','2_cpu_percentance_by_pod_300_2023-03-01 20:42:30.csv')

    # # Configurazione 3
    # main('3_latency_by_app_30s_300_2023-03-01 21:01:39.csv','3_cpu_percentance_by_pod_300_2023-03-01 21:01:39.csv')
    
    # # Configurazione 4
    # main('4_latency_by_app_30s_300_2023-03-04 14:36:48.csv','4_cpu_percentance_by_pod_300_2023-03-04 14:36:48.csv')
    
