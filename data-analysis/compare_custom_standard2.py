import logging
from matplotlib.ticker import MaxNLocator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# import plotly.graph_objs as go
# import plotly.io as pio

logging.basicConfig(level=logging.INFO)


def read_data(filename):
    try:
        df = pd.read_csv(filename, header=0)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")




def filter_data_node(df, ip_address, max_timestamp):
    filtered_df = df[(df['instance'] == ip_address)]
    filtered_df = filtered_df[filtered_df['timestamp']
                              <= pd.Timestamp(max_timestamp)]
    return filtered_df


def compare_node_cpu(cpu_1, cpu_2):
    cpu_1 = filter_data_node(cpu_1, '192.168.49.2:9100', '2023-03-11 17:06:16')
    cpu_2 = filter_data_node(cpu_2, '192.168.49.2:9100', '2023-03-05 16:14:54')

    time_range = np.arange(0, 2200, 5)

    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    
    ax1.plot(time_range, cpu_1['value'], label='HPA 1: Cpu based')
    ax1.plot(time_range, cpu_2['value'], label='HPA 2: Custom ')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('CPU Node (percentage)')


    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(time_range[::len(time_range)//8])
    ax2.set_xticklabels(cpu_1['users'].astype(
        int)[::len(cpu_1['users'].astype(int))//8])
    ax2.spines['top'].set_position(('outward', 20))
    ax2.spines['top'].set_color("navy")
    ax2.set_xlabel("Users (num)", color="navy")
    ax2.tick_params(axis='x', colors="navy")
    

    # make a legend for both plots
    leg = ax1.legend()
    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)

    plt.show()

def filter_data_replicas(df,max_timestamp):
    df = df[(df['deployment'] != 'prometheus-adapter')]
    df = df[df['timestamp']
                              <= pd.Timestamp(max_timestamp)]
    df = df.drop(columns=['__name__', 'instance','job','namespace'])
    
    pods = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
            "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart","shippingservice"]
    df_concat = pd.DataFrame()
    df_users = df[df['deployment'].str.contains('adservice')]['users']
    for pod in pods:
        df_tmp = df[df['deployment'].str.contains(pod)]
        df_tmp = df_tmp.drop(columns=['deployment'])
        df_concat = pd.concat([df_concat, df_tmp])
    
    df_sum = df_concat.groupby('timestamp')['value'].sum()
    return df_sum, df_users


def compare_replicas(replicas_1,replicas_2):
   
    replicas_1, replicas_1_users = filter_data_replicas(replicas_1, '2023-03-11 17:06:16')
    replicas_2, replicas_2_users= filter_data_replicas(replicas_2, '2023-03-05 16:14:54')
    
    time_range = np.arange(0, 2200, 5)

    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    ax1.plot(time_range, replicas_1, label='HPA: Custom 2')
    # ax1.plot(time_range, replicas_2, label='HPA 2: Custom ')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Available Replicas (num)')
    

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(time_range[::len(time_range)//8])
    ax2.set_xticklabels(replicas_1_users.astype(
        int)[::len(replicas_1_users.astype(int))//8])
    ax2.spines['top'].set_position(('outward', 20))
    ax2.spines['top'].set_color("navy")
    ax2.set_xlabel("Users (num)", color="navy")
    ax2.tick_params(axis='x', colors="navy")
   

    # make a legend for both plots
    leg = ax1.legend()
    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    plt.show()
def compare_rt(latency_df1,latency_df2):
    ts1 = latency_df1[(latency_df1['source_app'] == 'loadgenerator') & (
        latency_df1['destination_app'] == 'frontend')]
    
    ts1 = ts1[ts1['timestamp'] <= pd.Timestamp('2023-03-11 17:06:16')]
    ts2 = latency_df2[(latency_df2['source_app'] == 'loadgenerator') & (
        latency_df2['destination_app'] == 'frontend')]
    ts2 = ts2[ts2['timestamp'] <= pd.Timestamp('2023-03-05 16:14:54')]

    time_range = np.arange(0, 2200, 5)

    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    sloy = 1000 * np.ones(len(ts1.index))
    ax1.plot(time_range, ts1['value'], label='HPA 1: Cpu based')
    ax1.plot(time_range, ts2['value'], label='HPA 2: Custom ')
    ax1.plot(time_range, sloy, label='SLO')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Response Time (ms)')
    

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(time_range[::len(time_range)//8])
    ax2.set_xticklabels(ts1['users'].astype(
        int)[::len(ts1['users'].astype(int))//8])
    ax2.spines['top'].set_position(('outward', 20))
    ax2.spines['top'].set_color("navy")
    ax2.set_xlabel("Users (num)", color="navy")
    ax2.tick_params(axis='x', colors="navy")
   

    # make a legend for both plots
    leg = ax1.legend()
    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    plt.show()

def plot_all_replica(df):
    df = df[(df['deployment'] != 'prometheus-adapter')]
    df = df[df['timestamp']
                              <= pd.Timestamp('2023-03-05 16:14:54')]
    df = df.drop(columns=['__name__', 'instance','job','namespace'])
    
    pods = ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
            "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart","shippingservice"]
    
    time_range = np.arange(0, 2200, 5)

    for pod in pods:
        df_tmp = df[df['deployment'].str.contains(pod)]
        plt.plot(time_range, df_tmp['value'], label=f'{pod}')

    plt.xlabel('Time(s)')
    plt.ylabel('Available Replicas (num)')
    plt.legend()
    plt.show()
    



if __name__ == '__main__':

    # Read data from csv
    latency_df_5_1 = read_data(
        '5.1_latency_by_app_2m_300_2023-03-05 15:23:10.csv')
    cpu_df_5_1 = read_data(
        '5.1_node_cpu_percentance300_2023-03-05 15:23:10.csv')
    replicas_5_1 = read_data(
        '5.1_replicas_available_300_2023-03-05 15:23:10.csv')

    latency_df_5_2 = read_data(
        '5.2_latency_by_app_2m_300_2023-03-05 16:16:49.csv')
    cpu_df_5_2 = read_data(
        '5.2_node_cpu_percentance300_2023-03-05 16:16:49.csv')
    replicas_5_2 = read_data(
        '5.2_replicas_available_300_2023-03-05 16:16:49.csv')
    
    latency_df_5_3 = read_data(
        '5.3_latency_by_app_4m_300_2023-03-11 17:09:59.csv')
    cpu_df_5_3 = read_data(
        '5.3_node_cpu_percentance300_2023-03-11 17:09:59.csv')
    replicas_5_3 = read_data(
        '5.3_replicas_available_300_2023-03-11 17:09:59.csv')

    # compare_node_cpu(cpu_df_5_1, cpu_df_5_2)
    # compare_replicas(replicas_5_1,replicas_5_2)
    # compare_rt(latency_df_5_1,latency_df_5_2)
    # plot_all_replica(replicas_5_2)
    
    # compare_node_cpu(cpu_df_5_3, cpu_df_5_2)
    compare_replicas(replicas_5_3,replicas_5_2)
    # compare_rt(latency_df_5_3,latency_df_5_2)

