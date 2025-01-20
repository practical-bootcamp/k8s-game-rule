import logging
import time

import pytest
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


@pytest.mark.order(5)
class TestCheck:

    def test_001_pod_image_updated(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx"
        pod_namespace = "default"
        updated_image = "nginx:1.24.0"

        pods = k8s_client.list_namespaced_pod(namespace=pod_namespace)
        pod_info = next((pod for pod in pods.items if pod.metadata.name == pod_name), None)
        assert pod_info is not None, f"Pod '{pod_name}' does not exist in namespace '{pod_namespace}'"
        assert pod_info.spec.containers[0].image == updated_image, f"Pod image is not updated to '{updated_image}'"

    def test_002_pod_restarted(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        initial_restart_count = self.get_pod_restart_count(kube_config, pod_namespace="default", pod_name="nginx")
        
        # Wait a while for the pod to restart
        time.sleep(60)

        final_restart_count = self.get_pod_restart_count(kube_config, pod_namespace="default", pod_name="nginx")
        
        assert final_restart_count > initial_restart_count, "Pod did not restart after image update"

    def get_pod_restart_count(self, kube_config, pod_namespace, pod_name):
        command = f"kubectl get pod {pod_name} -n {pod_namespace} -o jsonpath='{{.status.containerStatuses[0].restartCount}}'"
        result = run_kubectl_command(kube_config, command)
        return int(result)
