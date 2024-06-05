import kopf
from prometheus_api_client import PrometheusConnect
from kubernetes import client, config

PROMETHEUS_URL = "http://wb-prometheus-kube-prometh-prometheus.monitoring.svc.cluster.local:9090"

def query_prometheus(query):
    prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)
    result = prom.custom_query(query=query)
    return result

def adjust_pod_resources(name, namespace, new_resources):
    api_instance = client.CoreV1Api()
    try:
        pod = api_instance.read_namespaced_pod(name=name, namespace=namespace)
        pod.spec.containers[0].resources = new_resources
        api_instance.replace_namespaced_pod(name=name, namespace=namespace, body=pod)
        print(f"Pod {name} in {namespace} has been adjusted.")
    except client.exceptions.ApiException as e:
        print(f"Exception when calling CoreV1Api->replace_namespaced_pod: {e}")

@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    config.load_incluster_config()
    settings.posting.level = 'INFO'

@kopf.timer('pods', interval=60)
def adjust_resources_periodically(namespace, name, logger, **kwargs):
    query = 'workload:adas_long_term_cpu_usage:q95_max_rate_1m'
    try:
        results = query_prometheus(query)
        for result in results:
            pod_namespace = result['metric'].get('namespace')
            pod_name = result['metric'].get('pod')
            cpu_usage = result['value'][1]

            new_resources = client.V1ResourceRequirements(
                requests={"cpu": f"{float(cpu_usage) * 1000}m"},
                limits={"cpu": f"{float(cpu_usage) * 2000}m"}
            )

            if pod_namespace == namespace and pod_name == name:
                adjust_pod_resources(pod_name, pod_namespace, new_resources)
    except Exception as e:
        logger.error(f"Exception when querying Prometheus: {e}")

if __name__ == '__main__':
    kopf.run()
