import subprocess
import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    
    def create_pod(self, k8s_client, pod_name):
        pod_manifest = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': pod_name,
                'labels': {
                    'app': 'v1'
                }
            },
            'spec': {
                'containers': [{
                    'name': 'nginx',
                    'image': 'nginx:1.24.0',
                    'ports': [{'containerPort': 80}]
                }]
            }
        }
        resp = k8s_client.create_namespaced_pod(
            body=pod_manifest,
            namespace='default')
        logging.info(f"Pod created: {resp.metadata.name}")
    
    def test_001_pod_attributes_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)

        pod_names = ["nginx1", "nginx2", "nginx3"]
        for pod_name in pod_names:
            self.create_pod(k8s_client, pod_name)
        
        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace='default')
            assert pod.spec.containers[0].image == "nginx:1.24.0", "Pod image version is not nginx:1.24.0"
            assert pod.spec.containers[0].ports[0].container_port == 80, "Pod containerPort is not 80"
            assert pod.metadata.namespace == "default", "Pod namespace is not default"
            assert pod.metadata.name == pod_name, "Pod name is not {}".format(pod_name)
            assert pod.metadata.labels["app"] == "v1", "Pod label app is not v1"

    def test_002_pod_attributes_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["$client_certificate"],
            json_input["$client_key"],
            json_input["$endpoint"],
        )

        pod_names = ["nginx1", "nginx2", "nginx3"]
        for pod_name in pod_names:
            command = f"kubectl get pod {pod_name} -n default -o json"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                logging.error(f"Command failed with error: {result.stderr}")
            else:
                json_output = result.stdout.strip()
                logging.info(json_output)
            
                pod_data = json.loads(json_output)
                
                assert pod_data["spec"]["containers"][0]["image"] == "nginx:1.24.0", "Pod image version is not nginx:1.24.0"
                assert pod_data["spec"]["containers"][0]["ports"][0]["containerPort"] == 80, "Pod containerPort is not 80"
                assert pod_data["metadata"]["namespace"] == "default", "Pod namespace is not default"
                assert pod_data["metadata"]["name"] == pod_name, f"Pod name is not {pod_name}"
                assert pod_data["metadata"]["labels"]["app"] == "v1", "Pod label app is not v1"
