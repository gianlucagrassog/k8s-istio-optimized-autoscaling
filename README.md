# k8s-istio-optimized-autoscaling
This Repo provides an in-depth analysis of the challenges involved in optimizing the performance of an microservices application through autoscaling, as well as potential solutions and best practices to address these challenges, and evaluate the possibility of employing an HPA  which uses application-specific metrics (the response time in percentiles of individual microservices), instead of the classic core metrics (CPU, memory).
<a name="readme-top"></a>

## Table of contents
* [Repository structure](#repository-structure)

* [Enviroment Configuration](#enviroment-configuration)
* [Requirements](#requirements) 
* [Solutions](#solutions)
	* [Load Testing Algorithms execution](#load-testing-algorithms-execution)
	* [Algorithms 1 & 2](#algorithms-1--2)
	* [HPA implementation with Custom Metrics](#hpa-implementation-with-custom-metrics)
	* [Results](#setup)


## Repository structure

- **Load Testing** 
 
	 The folder *loadtesting* contains the files needed for load testing  an microservice application with different signals (using Locust Framework).
	 *	**`load_testing_custom_shape.py`**:  Allows load testing using a custom input signal shape;
	*	 **`load_testing_ramp.py`**:  Allows load testing using a RAMP signal shape;
	
	The folder also contains an algorithm used to *find the number of pods* that can be specified as the max number in the HPA (Horizontal Pod Autoscaler):

	*  **`find_num_replica.py`**: Enables load testing of the application using a ramp signal for 10 min iteratively, evaluating performance  in terms of SLI (Response Time Percentiles and Availability) when adding a replica to a specific deployment of a microservice.
- **Data Analysis** 
The folder *data-analysis* contains the files needed for analyze the results of the load tests.
	 * **`find_rt_weight_of_ms.py`**: This algorithm allows to find out the impact of a microservice on latency, i.e. the percentage weight on high-level latency.
	 * **`data_plot.py`** and **`histograms.py`**: Thanks to this scrypts, data obtained as results of load testing scrypts can be plotted.

- **Load Generator Images**
Inside the *loadgenerator-src* folder there is the code of the load generator images used for load testing of the application.
Two versions are available:
	* *loadgenerator-v2 (RAMP)*: Uses a 10-minute ramp signal
	* *loadgenerator-v3 (Custom Shape)*: Uses a custom signal, proving the possibility of replicating a real production load, this load can be obtained in terms of requests per second by monitoring the application with the grafana dashboards provided.

 - **Grafana Dashboards** 
 The `grafana-dashboards` folder contains the the JSON files for Grafana dashboards, which can be used to monitor various metrics related to an application or system (i.e. the four golden signals). These dashboards can be used to monitor various metrics during load testing to identify anomalies and performance issues in the system.
 
- **HPA (Horizontal Pod Autoscaler) Config Files**
Inside the *hpa-yaml* folder there are the HPA configuration files applied to the microservices, including the one with the *Custom Metrics* (Response Time Percentiles).
 

	
## Enviroment Configuration 
 1. ***Establish a kubernetes cluster***
 
	 Establish a kubernetes cluster, necessary for the execution of the experiment. 
	 The cluster must be single-node and have  at least **12** **vCPU**, **12288 MB** (Megabytes) of RAM and **32** **GB** of disk space.
	This can be achieved by using tools such as minikube or kind.

	The following command, for example, represents the command needed to start a cluster with the given resources:
	```
	minikube start --cpus=12 --memory 12288 --disk-size 32g
	```
		   
 2. ***Install Istio Service mesh***
 		 For detailed instructions see [Istio documentation](https://istio.io/latest/docs/setup/getting-started/).
	```
	curl -L https://istio.io/downloadIstio | sh -

	cd istio-[istio-version]

	export PATH=$PWD/bin:$PATH

	istioctl install

	```
 4. ***Configure Istio***
 Add a namespace label to instruct Istio to automatically inject Envoy sidecar proxies.
	 ```
	 kubectl label namespace default istio-injection=enabled
	 ```

 3. ***Deploy a microservice application***
	 ```
	kubectl apply -f demo-application/kubernetes-manifests.yaml
	 ```
 5. ***Install Monitoring Tools***
 
     Apply Prometheus, Grafana and Kiali configuration files
	```
	kubectl apply -f tools/prometheus.yaml
	kubectl apply -f tools/grafana.yaml
	kubectl apply -f tools/kiali.yaml
	```
 6. ***Install software required for metric export***: 
	 
	 **kube-state-metrics**: (Required to obtain number of available replicas)
	Clone and apply manifests
	```
	git clone https://github.com/kubernetes/kube-state-metrics

	kubectl apply -f kube-state-metrics/examples/standard/

	```
	Add to scrape_configs (already configured in the file of prometheus provided)
	
	**Node Exporter**: (Required for cluster-related metrics)
	```
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

	helm repo update

	helm install node-exporter prometheus-community/prometheus-node-exporter
	```
	**Metrics-server**
	```
	minikube addons enable metrics-server
	```
		


## Requirements 

- *Load Testing Algoritms*
	* Install Python Libraries: `prometheus_api_client`,` pandas`
	There is no need to install the `Locust` library or other related libraries for the loadgenerator as the docker image will do it .
	* Set Enviroment variable `FRONTEND_ADDR` in loadgenerators yamls.
	* Build Load Generators Docker Images.
		```
		eval $(minikube docker-env);

		docker build -t loadgenerator:v1 ./loadgenerator-src/loadgenerator-v1/

		docker build -t loadgenerator:v2 ./loadgenerator-src/loadgenerator-v2/

		docker build -t loadgenerator:v3 ./loadgenerator-src/loadgenerator-v3/
		```

- *Data Analysis Algoritms*
	* Install Python Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`.
## Solutions
### Load Testing Algorithms execution

The first step is to *load test* the application using two different signals using the two scripts:
- **`load_testing_custom_shape.py`** e **`load_testing_ramp.py`**

	 * The shape used by *load_testing_custom_shape.py*  can be replaced by editing the *locust_file.py* file in the *loadgenerator_src/loadgenerator_v3* folder.  And must be obtained from monitoring the application, seeing how the production load behaves, request per seconds over time. 
	 
	* Port-forward Prometheus:
		```
		kubectl port-forward svc/prometheus -n istio-system 9090
		kubectl port-forward svc/grafana -n istio-system 3000
		kubectl port-forward svc/loadgenerator 8089
		kubectl port-forward svc/kiali -n istio-system  20001
		```

	* Start Algorithms
		```
		cd load-testing/
		```

		```
		python3 load_testing_custom_shape.py
		```
		or
		```
		python3 load_testing_ramp.py
		```


At the end of the load test, both algorithms export Prometheus metrics and the SLI (Service level Indicator) obtained in the simulation. These results can be analysed in order to make decisions on autoscaling strategy.


### Algorithms 1 & 2
- **`find_rt_weight_of_ms.py`**

	From the results of load testing scripts (*latency_by_app*), it analyses the latencies of flows between *pairs of microservices*.
	It obtains the weight each time stamp of the simulation and then relates it to the high-level latency value. As output, it provides a percentage value for each microservice.
	* Move csv to csv_results and Replace csv file names in Algorithm
	* Exec Algorithm:
		``` 
		cd data-analysis
		python find_rt_weight_of_ms.py
		```
	*	Example Output:
		```
		----- Top three MS ------
		Microservice Name : Value
		frontend :  59.22 %
		checkoutservice :  18.90 %
		currencyservice :  5.72 %
		```
		Thanks to its output, we can understand which microservice has the highest impact on latency.

- **`find_num_replica.py`**
	
	This algorithm is executed after the identification of the microservice on which to apply the HPA autoscaler (microservice with highest impact on latency ). 

	It allows to find the *number of replicas* to be applied by carrying out load testing using a ramp signal iteratively, assessing whether the insertion of additional replica results in a performance improvement in terms of SLI.


	![prova (3)](https://user-images.githubusercontent.com/93397222/233935130-d2839137-d561-4fe6-b1a5-a2d70db34f78.gif)

- **Configure HPAs**
	
	An HPA autoscaler can be applied, once the microservice with the highest impact on latency and the maximum number of pods to assign to it is obtained.


## HPA implementation with Custom Metrics


**Why Custom Metrics?**

The use of Custom Metrics makes it possible to achieve scalability based on the actual load of the application, which results in *greater scalability accuracy* than that based on CPU and memory.

**Which metrics to choose?**

It was decided to use the application's SLIs (Service Level Indicators) as Custom Metrics. The exposure of these metrics makes it possible to create a custom HPA, which performs the scaling procedures directly on the basis of the application's SLIs.


**Steps for hpa implementation using custom metrics**

1. Create a Prometheus Adapter Config File (A ready-to-deploy configuration file is provided)
2. Install prometheus adapter with Custom metrics.

	```
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

	helm repo update

	helm install -f prometheus-adapter-config.yaml prometheus-adapter prometheus-community/prometheus-adapter
	```
3. Create and Apply HPA with Custom Metrics



## Results

![Figure_10](https://github.com/gianlucagrassog/masterthesis-gg/assets/93397222/20e8150c-cf8f-43c0-96e2-f948752dd421  | width=100)
![Figure_4](https://github.com/gianlucagrassog/k8s-istio-optimized-autoscaling/assets/93397222/67ce9959-cf8d-43dd-bf6b-c87ff82b8ed8  | width=100 )
![Figure_10](https://github.com/gianlucagrassog/k8s-istio-optimized-autoscaling/assets/93397222/86a05db7-8fa9-469a-8e45-3f86dc4817c2 | width=100)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## University 

>[Unict](https://www.unict.it/) &nbsp;&middot;&nbsp;
>[LM-32  Corso di laurea magistrale in  Ingegneria Informatica](https://www.dieei.unict.it/corsi/lm-32)

## Contacts
> GitHub [@gianlucagrassog](https://github.com/gianlucagrassog) &nbsp;&middot;&nbsp;
> Linkedin [@gianlucagrassog](https://www.linkedin.com/in/gianlucagrassog/)
 
