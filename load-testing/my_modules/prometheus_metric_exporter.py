# █▀█ █▀█ █▀█ █▀▄▀█ █▀▀ ▀█▀ █░█ █▀▀ █░█ █▀
# █▀▀ █▀▄ █▄█ █░▀░█ ██▄ ░█░ █▀█ ██▄ █▄█ ▄█

# █▀▄▀█ █▀▀ ▀█▀ █▀█ █ █▀▀   █▀▀ ▀▄▀ █▀█ █▀█ █▀█ ▀█▀ █▀▀ █▀█
# █░▀░█ ██▄ ░█░ █▀▄ █ █▄▄   ██▄ █░█ █▀▀ █▄█ █▀▄ ░█░ ██▄ █▀▄

from datetime import datetime, timedelta
import csv,os
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
import logging
# import promql_constants 
import pandas as pd

def collect_metric(query, start_time, end_time, prom):
    metric_data = prom.custom_query_range(
        query = query,
        start_time=start_time,
        end_time=end_time,
        step=5
    )
    df = MetricRangeDataFrame(metric_data)
    # df = df.drop(columns=[
    #     'destination_app', 'source_app']).astype(int)
    df = df.fillna(0)
    
    return df

def collect_save_metric(query, start_time, end_time, metric_name, prom):
    logging.info('Collect Metric and Save Result')
    metric_data = prom.custom_query_range(
        query = query,
        start_time=start_time,
        end_time=end_time,
        step=5
    )
    print(metric_data)
    df = MetricRangeDataFrame(metric_data)
    dir_path = "results"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filepath = os.path.join(dir_path, f"{metric_name}.csv")
    with open(filepath, 'w+') as f:
        df.to_csv(f)


# if __name__ == '__main__':
#     prometheus_url = "http://localhost:9090"
#     prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)

#     start_time = parse_datetime("2023-03-12 12:11:48");
#     end_time = parse_datetime("2023-03-12 12:30:21");
#     # start_time = datetime.now()- timedelta(minutes=6)
#     # end_time = datetime.now()
#     print(start_time)
#     print(end_time)
    
#     name="6.2"
#     user_count=300
#     logging.info('aa')    
#     collect_save_metric(promql_constants.CPU_PERCENTANCE_BY_POD, start_time, end_time, f'{name}_cpu_percentance_by_pod_{user_count}_{end_time}',prometheus)
#     collect_save_metric(promql_constants.LATENCY_BY_APP,start_time, end_time, f'{name}_latency_by_app_{user_count}_{end_time}',prometheus)
#     collect_save_metric(promql_constants.LATENCY_BY_APP_30S, start_time, end_time, f'{name}_latency_by_app_30s_{user_count}_{end_time}',prometheus)
#     collect_save_metric(promql_constants.LATENCY_BY_APP_2M, start_time, end_time, f'{name}_latency_by_app_2m_{user_count}_{end_time}',prometheus)
#     collect_save_metric(promql_constants.MEMORY_USAGE_BY_POD, start_time, end_time, f'{name}_memory_usage_by_pod_{user_count}_{end_time}',prometheus)
#     collect_save_metric(promql_constants.REPLICAS_AVAILABLE, start_time, end_time, f'{name}_replicas_available_{user_count}_{end_time}',prometheus)
#     collect_save_metric(promql_constants.NODE_CPU_PERCENTANCE, start_time, end_time, f'{name}_node_cpu_percentance{user_count}_{end_time}',prometheus)
