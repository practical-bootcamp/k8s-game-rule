import pytest
import logging
from tests.helper.k8s_client_helper import configure_k8s_client

@pytest.mark.order(1)
def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)
    pod_names = ["nginx1", "nginx2", "nginx3"]
    pod_namespace = json_input["namespace"]

    for pod_name in pod_names:
        try:
            # 检查Pod是否已经存在
            k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            logging.info(f"Pod '{pod_name}' already exists in namespace '{pod_namespace}'")
        except Exception as e:
            # 如果Pod不存在，则创建它
            pod_manifest = {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {
                    "name": pod_name,
                    "labels": {
                        "app": "v1"
                    },
                    "namespace": pod_namespace
                },
                "spec": {
                    "containers": [{
                        "name": "nginx",
                        "image": "nginx:latest"
                    }]
                }
            }
            response = k8s_client.create_namespaced_pod(namespace=pod_namespace, body=pod_manifest)
            logging.info(f"Created Pod: {pod_name} response: {response}")
