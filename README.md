# k8s-istio-optimized-autoscaling

This Repo provides an in-depth analysis of the challenges involved in optimizing the performance of an microservices application through autoscaling, as well as potential solutions and best practices to address these challenges, and evaluate the possibility of employing an HPA  which uses application-specific metrics (the response time of individual microservices), instead of the classic core metrics (CPU, memory).

### Prerequisites
- *Kubernetes Cluster:* Single-node cluster with at least **12** **vCPU**, **12288 MB** (Megabytes) of RAM and **32** **GB** (Gigabytes) of storage memory.
- *Istio Service Mesh* installed.
- *Tools* deployed.
	* Prometheus (required), Grafana and Kiali (optional).
	* Prometheus Adapter (required for custom metric HPA)
	* Kube State Metrics
	* Node Exporter
	
	
### Load Testing
The folder *loadtesting* contains the files needed for load testing of the application.
 
 - **`find_num_replica.py`**: Used to find the number of pods that can be specified as the max number in the HPA. Enables load testing of the application using a ramp signal for 10 min iteratively, evaluating performance  in terms of SLI (Response Time Percentiles and Availability) when adding a replica to a specific deployment of a microservice. .
 *Script that is executed after the identification of the microservice on which to apply the HPA autoscaler, it allows us to find the number of replicas to be applied by carrying out load testing using a ramp signal iteratively, assessing whether the insertion of additional replica results in a performance improvement in terms of SLI.*
 
 - **`load_testing_custom_shape.py`**:  Allows load testing using a custom input signal shape;
	  This shape must be obtained from monitoring the application, seeing how the production load behaves, request per seconds over time. The signal can be replaced by editing the *locust_file.py* file in the *loadgenerator_images/loadgenerator_v3* folder.   At the end of load testing, metrics are exported from prometheus and the SLIs defined in the SLO document are displayed.
 
 - **`load_testing_ramp.py`**:  Allows load testing using a RAMP signal shape;  At the end of load testing, metrics are exported from prometheus and the SLIs defined in the SLO document are displayed and saved.


These scripts make use of a series of purpose-built modules within *my_modules*, each of which has a specific function:
 - `prometheus_metric_exporter.py`: This file can be used to export and optionally save metrics from a Prometheus server in CSV files.
 - `promql_constants.py` : All the constants used to perform promQL queries are defined within it, they are the metrics that are extracted from Prometheus
 - `operations.py`:  File containing all the operations that make it possible to load, modify  and apply Load Generator files; and also exec commands .

Inside the *src* folder there is the code of the load generator images used for load testing of the application

### Grafana Dashboard

 The `grafana-dashboards` folder contains the the JSON files for Grafana dashboards, which can be used to monitor various metrics related to an application or system (i.e. the four golden signals).
These dashboards can be used to monitor various metrics during load testing to identify anomalies and performance issues in the system.
 
 - *Monitoring SLI Istio Microservices* : Dashboard to monitor the measured SLIs, these SLIs were described in an SLO document.
 -  *Monitoring Four Golden Signals*: Dashboard used during load test execution to monitor the application.
 
 
### Data Analysis

### Istio Service Mesh

### Custom Metrics Autoscaler

### Tools

#### Prometheus and Grafana 
```
kubectl apply -f tools/prometheus.yaml
kubectl apply -f tools/grafana.yaml
```
```
kubectl port-forward svc/prometheus -n istio-system 9090

kubectl port-forward svc/grafana -n istio-system 3000
```
#### Kube State metrics

```
git clone https://github.com/kubernetes/kube-state-metrics

kubectl apply -f kube-state-metrics/examples/standard/
```


```
- job_name: 'kube-state-metrics'
	static_configs:
		- targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']
```
#### Node Exporter
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

helm install node-exporter prometheus-community/prometheus-node-exporter
```
