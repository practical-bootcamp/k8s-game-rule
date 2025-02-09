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
        namespace = json_input["namespace"]

        try:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get Pod '{pod_name}': {str(e)}"

        # 验证Pod的内容
        assert pod.api_version == "v1", "Incorrect apiVersion."
        assert pod.kind == "Pod", "Incorrect kind."
        assert pod.metadata.name == pod_name, "Incorrect metadata.name."

        # 检查Pod的securityContext
        security_context = pod.spec.containers[0].security_context
        assert security_context is not None, "Missing securityContext in Pod."
        assert "NET_ADMIN" in security_context.capabilities.add, "Missing capability 'NET_ADMIN' in Pod securityContext."
        assert "SYS_TIME" in security_context.capabilities.add, "Missing capability 'SYS_TIME' in Pod securityContext."

        logging.info(f"Pod '{pod_name}' has the correct securityContext capabilities 'NET_ADMIN' and 'SYS_TIME'.")

    def test_002_check_pod_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_pod_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get pod nginx-pod -n {json_input['namespace']} -o json"
        result = run_kubectl_command(kube_config, command)
        pod = json.loads(result)

        # 验证Pod的内容
        assert pod["apiVersion"] == "v1", "Incorrect apiVersion."
        assert pod["kind"] == "Pod", "Incorrect kind."
        assert pod["metadata"]["name"] == "nginx-pod", "Incorrect metadata.name."

        # 检查Pod的securityContext
        security_context = pod["spec"]["containers"][0]["securityContext"]
        assert security_context is not None, "Missing securityContext in Pod."
        assert "NET_ADMIN" in security_context["capabilities"]["add"], "Missing capability 'NET_ADMIN' in Pod securityContext."
        assert "SYS_TIME" in security_context["capabilities"]["add"], "Missing capability 'SYS_TIME' in Pod securityContext."

        logging.info(f"Pod 'nginx-pod' has the correct securityContext capabilities 'NET_ADMIN' and 'SYS_TIME'.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
