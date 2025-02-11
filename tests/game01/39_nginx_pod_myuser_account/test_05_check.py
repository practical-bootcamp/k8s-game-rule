import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_pod_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx-pod"
        namespace = "default"

        try:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get Pod '{pod_name}': {str(e)}"

        # 验证Pod的内容
        assert pod.api_version == "v1", "Incorrect apiVersion."
        assert pod.kind == "Pod", "Incorrect kind."
        assert pod.metadata.name == pod_name, "Incorrect metadata.name."
        assert pod.metadata.namespace == namespace, "Incorrect metadata.namespace."
        assert pod.spec.service_account_name == "myuser", "Pod is not using the correct ServiceAccount."

        logging.info(f"Pod '{pod_name}' in Namespace '{namespace}' is using ServiceAccount 'myuser'.")

    def test_002_check_pod_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_pod_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get pod nginx-pod -n default -o json"
        result = run_kubectl_command(kube_config, command)
        pod = json.loads(result)

        # 验证Pod的内容
        assert pod["apiVersion"] == "v1", "Incorrect apiVersion."
        assert pod["kind"] == "Pod", "Incorrect kind."
        assert pod["metadata"]["name"] == "nginx-pod", "Incorrect metadata.name."
        assert pod["metadata"]["namespace"] == "default", "Incorrect metadata.namespace."
        assert pod["spec"]["serviceAccountName"] == "myuser", "Pod is not using the correct ServiceAccount."

        logging.info(f"Pod 'nginx-pod' in Namespace 'default' is using ServiceAccount 'myuser'.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
