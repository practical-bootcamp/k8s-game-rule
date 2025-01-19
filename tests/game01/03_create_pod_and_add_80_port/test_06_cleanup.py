import logging

import pytest

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command
from tests.helper.k8s_client_helper import configure_k8s_client


@pytest.mark.order(6)
class TestCleanup:
    def test_delete_pod_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx"
        pod_namespace = "default"

        # 删除指定的 Pod
        response = k8s_client.delete_namespaced_pod(
            name=pod_name,
            namespace=pod_namespace,
            body={}
        )
        logging.info(response)
        assert response.status == "Success", f"Failed to delete Pod '{pod_name}' in namespace '{pod_namespace}'"

    def test_delete_pod_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        pod_name = "nginx"
        pod_namespace = "default"

        # 使用 kubectl 命令删除 Pod
        command = f"kubectl delete pod {pod_name} -n {pod_namespace}"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)

        assert f"pod \"{pod_name}\" deleted" in result, f"Pod '{pod_name}' was not deleted successfully"