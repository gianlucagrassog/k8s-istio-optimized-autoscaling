# █▀▀ █ █▄░█ █▀▄   █▄░█ █░█ █▀▄▀█ █▄▄ █▀▀ █▀█
# █▀░ █ █░▀█ █▄▀   █░▀█ █▄█ █░▀░█ █▄█ ██▄ █▀▄

# █▀█ █▀▀   █▀█ █▀▀ █▀█ █░░ █ █▀▀ ▄▀█ █▀
# █▄█ █▀░   █▀▄ ██▄ █▀▀ █▄▄ █ █▄▄ █▀█ ▄█
import logging
from datetime import datetime, timedelta
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame
import pandas as pd
import time

# Import my_modules
from my_modules.prometheus_metric_exporter import collect_metric, collect_save_metric
from my_modules.promql_constants import *
from my_modules.operations import *

# Set up Prometheus API client and logging
prometheus = PrometheusConnect(url='http://localhost:9090', disable_ssl=True)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def check_sli(start_time):

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

    # Return Percentile and Availability
    return percentile99, percentile90, percentile50, availability

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

def main(deploy):
    logging.info('Starting load tests')
    p99_last, p90_last, p50_last, availability_last = 0,0,0,0

    for num_replica in range(1, 10):
        logging.info(
            f'Starting load test with {num_replica} replica on {deploy}')
        time.sleep(15)

        # Scale deployment to num_replica
        scale_deploy(deploy, num_replica)

        yaml_filepath = 'loadgenerator.yaml'
        apply_yaml_file(yaml_filepath)

        start_time = datetime.now()
        test_interval_time = 600
        time.sleep(test_interval_time)
        apply_yaml_file('loadgenerator-reset.yaml')

        # Check if there were any improvements in terms of SLI

        # Get current SLI metrics
        p99_current, p90_current, p50_current, availability_current = check_sli(
            start_time)
        if p99_current != 0 and p99_current != 0 and p50_current != 0 and availability_current != 0:

            # Calculate the percentage change for each metric
            p99_percent_change = ((p99_current - p99_last) / p99_last) * 100
            p90_percent_change = ((p90_current - p90_last) / p90_last) * 100
            p50_percent_change = ((p50_current - p50_last) / p50_last) * 100
            availability_percent_change = (
                (availability_current - availability_last) / availability_last) * 100

            # Check if there were any improvements
            if p99_percent_change < 0 or p90_percent_change < 0 or p50_percent_change < 0 or availability_percent_change > 0:
                logging.info("There were improvements in SLIs!")
            else:
                logging.info("There were no improvements in SLIs.")
            logging.info(f"- p99: {p99_percent_change}%")
            logging.info(f"- p90: {p90_percent_change}%")
            logging.info(f"- p50: {p50_percent_change}%")
            logging.info(f"- availability: {p50_percent_change}%")


if __name__ == '__main__':
    # main("frontend")
    main("checkoutservice")