# █▀█ █▀█ █▀█ █▀▄▀█ █▀█ █░░   █▀▀ █▀█ █▄░█ █▀ ▀█▀ ▄▀█ █▄░█ ▀█▀ █▀
# █▀▀ █▀▄ █▄█ █░▀░█ ▀▀█ █▄▄   █▄▄ █▄█ █░▀█ ▄█ ░█░ █▀█ █░▀█ ░█░ ▄█


# SLIs 10M
PERCENTILE_99TH_10M="histogram_quantile(0.99,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[10m]))"
PERCENTILE_90TH_10M="histogram_quantile(0.90,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[10m]))"
PERCENTILE_50TH_10M="histogram_quantile(0.50,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[10m]))"
AVAILABILITY_10M="sum(rate(istio_requests_total{reporter=\"source\", response_code!~\"5.*\"}[10m]))/sum(rate(istio_requests_total{reporter=\"source\"}[10m]))"

# SLIs 20M
PERCENTILE_99TH_20M="histogram_quantile(0.99,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[20m]))"
PERCENTILE_90TH_20M="histogram_quantile(0.90,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[20m]))"
PERCENTILE_50TH_20M="histogram_quantile(0.50,rate(istio_request_duration_milliseconds_bucket{reporter='source',response_code=\"200\", response_flags=\"-\", source_app=\"loadgenerator\",destination_app=\"frontend\"}[20m]))"
AVAILABILITY_20M="sum(rate(istio_requests_total{reporter=\"source\", response_code!~\"5.*\"}[20m]))/sum(rate(istio_requests_total{reporter=\"source\"}[20m]))"

# LATENCY of microservices
LATENCY_LG_FE="sum(rate(istio_request_duration_milliseconds_sum{reporter='source',source_app='loadgenerator',destination_app='frontend'}[1m])) by (source_app, destination_app) / sum(rate(istio_request_duration_milliseconds_count{reporter='source', source_app='loadgenerator',destination_app='frontend'}[1m])) by (source_app, destination_app)"
LATENCY_BY_APP_30S="sum(rate(istio_request_duration_milliseconds_sum{reporter='source'}[30s])) by (source_app, destination_app) / sum(rate(istio_request_duration_milliseconds_count{reporter='source', destination_app!='unknown'}[30s])) by (source_app, destination_app)"

# CPU and MEMORY
CPU_PERCENTANCE_BY_POD="sum(irate(container_cpu_user_seconds_total{id=~'/kubepods/burstable/.*',pod!=''}[1m])) by (pod) * 200"
MEMORY_USAGE_BY_POD="round(sum(irate(container_memory_usage_bytes{id=~'/kubepods/burstable/.*',pod!=''}[1m])) by (pod) / 1e5, 2)"

# REPLICAS (num pod per deployment)
REPLICAS_AVAILABLE="kube_deployment_status_replicas_available{namespace='default',deployment!='kube-state-metrics'}"

# NODE CPU and ERRORS
NODE_CPU_PERCENTANCE="100 - (avg by(instance) (rate(node_cpu_seconds_total{mode='idle'}[2m])) * 100)"
ISTIO_5XX_REQUESTS='sum(irate(istio_requests_total{reporter="source", response_code=~"5.*"}[2m])) by (source_app, destination_app)'

# LATENCY by app 1M, 2M, 4M
LATENCY_BY_APP="sum(rate(istio_request_duration_milliseconds_sum{reporter='source'}[1m])) by (source_app, destination_app) / sum(rate(istio_request_duration_milliseconds_count{reporter='source', destination_app!='unknown'}[1m])) by (source_app, destination_app)"
LATENCY_BY_APP_2M="sum(rate(istio_request_duration_milliseconds_sum{reporter='source'}[2m])) by (source_app, destination_app) / sum(irate(istio_request_duration_milliseconds_count{reporter='source', destination_app!='unknown'}[2m])) by (source_app, destination_app)"
LATENCY_BY_APP_4M="sum(rate(istio_request_duration_milliseconds_sum{reporter='source',source_app='loadgenerator',destination_app='frontend'}[4m])) by (source_app, destination_app) / sum(rate(istio_request_duration_milliseconds_count{reporter='source', source_app='loadgenerator',destination_app='frontend'}[4m])) by (source_app, destination_app)"

