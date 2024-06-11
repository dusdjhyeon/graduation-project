import kopf
from prometheus_api_client import PrometheusConnect
from kubernetes import client, config

PROMETHEUS_URL = "http://wb-prometheus-kube-prometh-prometheus.monitoring.svc.cluster.local:9090"

def query_prometheus(query):
    prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)
    result = prom.custom_query(query=query)
    return result

def adjust_task_resources(workflow_name, namespace, task_name, new_resources):
    api_instance = client.CustomObjectsApi()
    group = 'argoproj.io'
    version = 'v1alpha1'
    plural = 'workflows'

    # Woking if pod_name==workflow_task_name
    try:
        workflow = api_instance.get_namespaced_custom_object(group, version, namespace, plural, workflow_name)
        for template in workflow['spec']['templates']:
            if template['name'] == task_name:
                template['container']['resources'] = new_resources
        
        api_instance.replace_namespaced_custom_object(group, version, namespace, plural, workflow_name, workflow)
        print(f"Workflow {workflow_name} in {namespace} has been adjusted.")
    except client.exceptions.ApiException as e:
        print(f"Exception when calling CustomObjectsApi->replace_namespaced_custom_object: {e}")

@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    config.load_incluster_config()
    settings.posting.level = 'INFO'

@kopf.timer('workflows', interval=60)
def adjust_resources_periodically(namespace, name, logger, **kwargs):
    query = 'workload:adas_long_term_cpu_usage:q95_max_rate_1m'
    try:
        results = query_prometheus(query)
        for result in results:
            workflow_namespace = result['metric'].get('namespace')
            workflow_name = result['metric'].get('workflow')
            task_name = result['metric'].get('pod')  
            cpu_usage = result['value'][1]

            new_resources = {
                "requests": {"cpu": f"{float(cpu_usage) * 1000}m"},
                "limits": {"cpu": f"{float(cpu_usage) * 2000}m"}
            }

            if workflow_namespace == namespace and workflow_name == name:
                adjust_task_resources(workflow_name, workflow_namespace, task_name, new_resources)
    except Exception as e:
        logger.error(f"Exception when querying Prometheus: {e}")

if __name__ == '__main__':
    kopf.run()
