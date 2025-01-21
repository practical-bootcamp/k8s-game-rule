# test_05_check.py
import asyncio
import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

async def list_pods(k8s_client, namespace):
    return k8s_client.list_namespaced_pod(namespace=namespace)

@pytest.mark.order(5)
@pytest.mark.asyncio
class TestCheck:
    async def test_001_pods_exist_with_library(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_names = ["nginx1", "nginx2", "nginx3"]
        pod_namespace = json_input["namespace"]

        pods = await list_pods(k8s_client, pod_namespace)
        pod_list = {pod.metadata.name: pod.metadata.labels for pod in pods.items}

        for pod_name in pod_names:
            assert pod_name in pod_list, f"Pod '{pod_name}' does not exist in namespace '{pod_namespace}'"
            assert pod_list[pod_name]["app"] == "v1", f"Pod '{pod_name}' does not have label 'app=v1'"

    async def test_002_pods_exist_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], 
            json_input["key_file"],
            json_input["host"]
        )
        command = "kubectl get pods -n default -o json"
        result = await asyncio.to_thread(run_kubectl_command, kube_config, command)
        logging.info(result)
        
        pod_data = json.loads(result)
        pod_names = ["nginx1", "nginx2", "nginx3"]

        for pod in pod_data["items"]:
            if pod["metadata"]["name"] in pod_names:
                pod_names.remove(pod["metadata"]["name"])
                assert pod["metadata"]["labels"]["app"] == "v1", f"Pod '{pod['metadata']['name']}' does not have label 'app=v1'"
        
        assert not pod_names, "Some of the required Pods are missing"
