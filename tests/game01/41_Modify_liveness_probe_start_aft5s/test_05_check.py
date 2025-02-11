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

        # 检查livenessProbe
        container = pod.spec.containers[0]
        liveness_probe = container.liveness_probe
        assert liveness_probe.exec.command == ["ls"], "Incorrect liveness probe command."
        assert liveness_probe.initial_delay_seconds == 5, "Incorrect initialDelaySeconds for liveness probe."
        assert liveness_probe.period_seconds == 5, "Incorrect periodSeconds for liveness probe."

        logging.info(f"Pod '{pod_name}' in Namespace '{namespace}' has the correct liveness probe.")

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

        # 检查livenessProbe
        container = pod["spec"]["containers"][0]
        liveness_probe = container["livenessProbe"]
        assert liveness_probe["exec"]["command"] == ["ls"], "Incorrect liveness probe command."
        assert liveness_probe["initialDelaySeconds"] == 5, "Incorrect initialDelaySeconds for liveness probe."
        assert liveness_probe["periodSeconds"] == 5, "Incorrect periodSeconds for liveness probe."

        logging.info(f"Pod 'nginx-pod' in Namespace 'default' has the correct liveness probe.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
