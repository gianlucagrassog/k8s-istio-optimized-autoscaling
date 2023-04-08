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
import pandas as pd

from promql_constants import *


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


if __name__ == '__main__':
    prometheus_url = "http://localhost:9090"
    prometheus = PrometheusConnect(url=prometheus_url, disable_ssl=True)

    start_time = parse_datetime("2023-03-24 11:56:54")
    end_time = parse_datetime("2023-03-24 12:16:59")

    start_time1 = parse_datetime("2023-03-24 11:56:56")
    end_time1 = parse_datetime("2023-03-24 12:17:22")

    name="post_export_1"
    # collect_save_metric(REPLICAS_AVAILABLE, start_time, end_time, f'{name}.1_replicas_available_custom_shape_{datetime.now()}',prometheus)
    # collect_save_metric(REPLICAS_AVAILABLE, start_time1, end_time1, f'{name}.2_replicas_available_custom_shape_{datetime.now()}',prometheus)

    histo50="histogram_quantile(0.50,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[30s]))"
    histo90="histogram_quantile(0.90,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[30s]))"
    histo99="histogram_quantile(0.99,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[30s]))"
    
    collect_save_metric(histo50, start_time1, end_time1, f'{name}.histogram_quantile_0.50_{datetime.now()}',prometheus)
    collect_save_metric(histo90, start_time1, end_time1, f'{name}.histogram_quantile_0.90_{datetime.now()}',prometheus)
    collect_save_metric(histo99, start_time1, end_time1, f'{name}.histogram_quantile_0.99_{datetime.now()}',prometheus)


    