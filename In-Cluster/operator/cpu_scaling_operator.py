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


if __name__ == '__main__':
    kopf.run()
