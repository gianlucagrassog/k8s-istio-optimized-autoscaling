# █▀▀ █ █▄░█ █▀▄   █▀█ ▀█▀  
# █▀░ █ █░▀█ █▄▀   █▀▄ ░█░  

# █░█░█ █▀▀ █ █▀▀ █░█ ▀█▀   █▀█ █▀▀   █▀▄▀█ █▀
# ▀▄▀▄▀ ██▄ █ █▄█ █▀█ ░█░   █▄█ █▀░   █░▀░█ ▄█

import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

from my_modules.data_csv import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def find_weight_ms(latency_df, ms_names):
    # Dictionary for all latencies df
    latencies_of_mscouple = {}

    # Iterate all couple of ms
    for source in ms_names:
        for destination in ms_names:
            ts = latency_df[(latency_df['source_app'] == source) & (
                latency_df['destination_app'] == destination)]
            key = source + '_' + destination

            if not ts.empty:
                latencies_of_mscouple[key] = ts
    print(latency_df)
    print(type(latency_df))
    print(type(latencies_of_mscouple))
    print(type(latencies_of_mscouple['loadgenerator_frontend']))

    # Calculate all latency contributions in milliseconds for every microservice
    # lc_of_ms(t) = RT inbound flows[t] - RT outflows[t] for every timestamp
    lc_of_ms = {ms_name: {} for ms_name in ms_names}

    for i in range(len(ms_names)):
        ms_name = ms_names[i]

        for key in latencies_of_mscouple:
            source, destination = key.split('_')
            df = latencies_of_mscouple[key]

            if destination == ms_name:
                for index, row in df.iterrows():
                    timestamp = row['timestamp']
                    if not pd.isnull(row['value']):
                        if timestamp not in lc_of_ms[ms_name]:
                            lc_of_ms[ms_name][timestamp] = row['value']
                        else:
                            lc_of_ms[ms_name][timestamp] += row['value']

            if source == ms_name:
                for index, row in df.iterrows():
                    timestamp = row['timestamp']
                    if not pd.isnull(row['value']):
                        if timestamp not in lc_of_ms[ms_name]:
                            lc_of_ms[ms_name][timestamp] = row['value']
                        else:
                            lc_of_ms[ms_name][timestamp] -= row['value']

    # Extract High Level latency loadgenerator --> frontend
    latency_general = latency_df[(latency_df['source_app'] == "loadgenerator") & (
        latency_df['destination_app'] == "frontend")]

    # Calculate ratio percentage and mean
    # percentage result for a timestamp = (contribution / high level latency) *100
    weights_pg_ms={}

    for ms_name in lc_of_ms:
        p = []
        for row in lc_of_ms[ms_name]:
            ts = latency_general[latency_general['timestamp'] == row]
            if len(ts) > 1:
                ts = ts.nlargest(1, 'value')

            result = ((((lc_of_ms[ms_name][row])/ts['value'].values))*100)
            if result.size > 0:
                p.append(result[0])

        p = np.array(p)
        
        if p.size != 0 and ms_name!='loadgenerator':
            # Calculate Percentance weight mean
            mean = p.mean()
            weights_pg_ms[ms_name] = mean
            # logging.info(f'{ms_name} - '+" {:.2f} %".format(mean))
        
    return weights_pg_ms

def top_three_ms(weights_pg_ms):
    x=list(weights_pg_ms.values())
    x.sort(reverse=True)
    x=x[:3]
    print("----- Top three MS ------")
    print("Microservice Name : Value")
    for i in x:
        for j in weights_pg_ms.keys():
            if(weights_pg_ms[j]==i):
                print(str(j)+" : "+str(" {:.2f} %".format(weights_pg_ms[j])))
    

def main(latency_by_app_csv, ms_names):
    
    # Read data from csv
    latency_df = read_data(latency_by_app_csv)

    # Find Median Weight of microservices
    weights_pg_ms = find_weight_ms(latency_df, ms_names)

    # Find Top Three MS
    top_three_ms(weights_pg_ms)


if __name__ == '__main__':
    ms_names = ["frontend", "adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice",
                "paymentservice", "loadgenerator", "productcatalogservice", "recommendationservice", "shippingservice", "redis-cart"]
    
    # Config 1
    # main('./csv_results/config1/latency_by_app_custom_shape_23042023_144349.csv', ms_names)
    # main('./csv_results/latency_by_app_ramp_20ghfc230324114317.csv', ms_names)

    # # Config 2: HPA on Frontend
    main('./csv_results/config2/latency_by_app_custom_shape_09052023_203706.csv', ms_names)
    # main('./csv_results/latency_by_app_ramp_20230401144242.csv', ms_names)

