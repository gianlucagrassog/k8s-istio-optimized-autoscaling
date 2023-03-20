# k8s-istio-optimized-autoscaling

This Repo provides an in-depth analysis of the challenges involved in optimizing the performance of an microservices application through autoscaling, as well as potential solutions and best practices to address these challenges.
### Prerequisites

  
### Load Testing
The folder `loadtesting` contains the files needed for load testing of the application.

 - **load_testing_custom_shape.py**
 - **`find_num_replica.py`**: enables load testing of the application using a ramp signal for 10 min iteratively, evaluating performance when adding a replica.
 *Script that is executed after the identification of the microservice on which to apply the HPA autoscaler (using the data_analysis.py script), it allows us to find the number of replicas to be applied by carrying out load testing using a ramp signal iteratively, assessing whether the insertion of additional replica results in a performance improvement in terms of SLI.*
 
 - List item
 - 
All these scripts make use of a series of purpose-built modules within *my_modules*, each of which has a specific function:
 - `prometheus_metric_exporter.py`
 - `promql_constants.py`
 - `yaml_operations.py`
### Data Analysis
