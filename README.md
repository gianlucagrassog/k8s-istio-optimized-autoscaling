# k8s-istio-optimized-autoscaling

This Repo provides an in-depth analysis of the challenges involved in optimizing the performance of an microservices application through autoscaling, as well as potential solutions and best practices to address these challenges.

### Prerequisites
...
### Load Testing
The folder *loadtesting* contains the files needed for load testing of the application.

 - **`load_testing_custom_shape.py`**:  Allows load testing using a custom input signal shape;
	  This shape must be obtained from monitoring the application, seeing how the production load behaves, request per seconds over time. The signal can be replaced by editing the *locust_file.py* file in the *src/loadgenerator_custom_shape* folder.   At the end of load testing, metrics are exported from prometheus and the SLIs defined in the SLO document are displayed.
 
 - **`find_num_replica.py`**: Enables load testing of the application using a ramp signal for 10 min iteratively, evaluating performance when adding a replica to a specific microservice.
 *Script that is executed after the identification of the microservice on which to apply the HPA autoscaler (using the data_analysis.py script), it allows us to find the number of replicas to be applied by carrying out load testing using a ramp signal iteratively, assessing whether the insertion of additional replica results in a performance improvement in terms of SLI.*
 

These scripts make use of a series of purpose-built modules within *my_modules*, each of which has a specific function:
 - `prometheus_metric_exporter.py`: This file can be used to export and save metrics from a Prometheus server in CSV files.
 - `promql_constants.py` : All the constants used to perform promQL queries are defined within it, they are the metrics that are extracted from Prometheus
 - `yaml_operations.py`:  File containing all the operations that make it possible to load, modify  and apply Load Generator files.

### Grafana Dashboard

 The `grafana-dashbords` folder contains the the JSON files for Grafana dashboards, which can be used to monitor various metrics related to an application or system (i.e. the four golden signals).
These dashboards can be used to monitor various metrics during load testing to identify anomalies and performance issues in the system.
 
### Data Analysis

### Tools
