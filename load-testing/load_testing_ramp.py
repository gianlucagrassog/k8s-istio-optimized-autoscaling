# █░░ █▀█ ▄▀█ █▀▄   ▀█▀ █▀▀ █▀ ▀█▀ █ █▄░█ █▀▀
# █▄▄ █▄█ █▀█ █▄▀   ░█░ ██▄ ▄█ ░█░ █ █░▀█ █▄█

# █▀█ ▄▀█ █▀▄▀█ █▀█
# █▀▄ █▀█ █░▀░█ █▀▀

import logging
from datetime import datetime, timedelta
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame
import pandas as pd
import time
import csv, os



from my_modules.prometheus_metric_exporter import collect_metric, collect_save_metric
from my_modules.promql_constants import *
from my_modules.operations import *

# Set up Prometheus API client and logging
prometheus = PrometheusConnect(url='http://localhost:9090', disable_ssl=True)
logging.basicConfig(
    filename="log_ramp",
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def check_save_sli(start_time):
    # Collect Metrics from Prometheus
    percentile99 = collect_metric(
        PERCENTILE_99TH_10M, start_time, datetime.now(), prometheus)
    percentile90 = collect_metric(
        PERCENTILE_90TH_10M, start_time, datetime.now(), prometheus)
    percentile50 = collect_metric(
        PERCENTILE_50TH_10M, start_time, datetime.now(), prometheus)
    availability = collect_metric(
        AVAILABILITY_10M, start_time, datetime.now(), prometheus)
    
    # Extract Last Value
    percentile99 = percentile99['value'].iloc[-1]
    percentile90 = percentile90['value'].iloc[-1]
    percentile50 = percentile50['value'].iloc[-1]
    availability = availability['value'].iloc[-1]
    logging.info(
        f"##### SLI Check ##### \n - 99th Percentile: {percentile99} ms\n - 90th Percentile: {percentile90} ms\n - 50th Percentile: {percentile50} ms\n - Availability:{availability}")
    
   
    # Save metrics (Percentiles and Availability) to CSV file 
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    dir_path = "results"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filepath = os.path.join(dir_path, f"sli_ramp_{timestamp}.csv")
    with open(filepath, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', '99th_percentile', '90th_percentile', '50th_percentile', 'availability']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         '99th_percentile': percentile99,
                         '90th_percentile': percentile90,
                         '50th_percentile': percentile50,
                         'availability': availability})

# Check for 5xx errors in the last minutes
def check_errors(threshold=3):
    logging.info(f'Checking for 5xx errors with threshold {threshold}')
    query = ISTIO_5XX_REQUESTS
    metric_data = prometheus.custom_query(query=query)
    if metric_data:
        metric_df = MetricSnapshotDataFrame(metric_data)
        metric_df['value'] = pd.to_numeric(metric_df['value'])
        error_df = metric_df.loc[metric_df['value'] > threshold]
        if error_df.empty:
            logging.info('No 5xx errors found')
        else:
            logging.warning('5xx errors found:')
            logging.warning(error_df)
        return not error_df.empty
    return False

# Main function that runs the load tests for finnd num of replicas
def main():

    logging.info(f'Starting load test with RAMP signal for 10 Minutes')
    time.sleep(15)
  
    # Apply Load generator
    yaml_filepath = 'loadgenerator.yaml'
    apply_yaml_file(yaml_filepath)

    start_time = datetime.now()
    test_interval_time = 600
    time.sleep(test_interval_time)
    apply_yaml_file('loadgenerator-reset.yaml')
    

    # Check and Save SLI
    check_save_sli(start_time)
    
    # Check for errors
    check_errors()
    
    # Retrieve and Save metrics
    logging.info('Retrieve and save a metrics values ')
    timestamp = datetime.now()
    collect_save_metric(LATENCY_BY_APP_30S, start_time, timestamp,f'latency_by_app_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}', prometheus)
    collect_save_metric(CPU_PERCENTANCE_BY_POD, start_time, timestamp,f'cpu_percentance_by_pod_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}', prometheus)
    # collect_save_metric(MEMORY_USAGE_BY_POD, start_time, timestamp,f'memory_usage_by_pod_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}', prometheus)
    collect_save_metric(REPLICAS_AVAILABLE, start_time, timestamp,f'replicas_available_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}', prometheus)
    collect_save_metric(NODE_CPU_PERCENTANCE, start_time, timestamp,f'node_cpu_percentance_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}', prometheus)
    # collect_save_metric(HISTO_50, start_time, timestamp, f'histogram_quantile_0_50_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}',prometheus)
    # collect_save_metric(HISTO_90, start_time, timestamp, f'histogram_quantile_0_90_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}',prometheus)
    # collect_save_metric(HISTO_99, start_time, timestamp, f'histogram_quantile_0_99_ramp_{timestamp.strftime("%d%m%Y_%H%M%S")}',prometheus)
    logging.info('Load test finished')

if __name__ == '__main__':
    main()
