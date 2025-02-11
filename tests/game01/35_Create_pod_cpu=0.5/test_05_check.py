import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_pod_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_name = "resource-pod"
        namespace = "one"

        try:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get Pod '{pod_name}': {str(e)}"

        # 验证Pod的内容
        assert pod.api_version == "v1", "Incorrect apiVersion."
        assert pod.kind == "Pod", "Incorrect kind."
        assert pod.metadata.name == pod_name, "Incorrect metadata.name."
        assert pod.metadata.namespace == namespace, "Incorrect metadata.namespace."

        # 检查Pod的资源请求和限制
        container = pod.spec.containers[0]
        resources = container.resources
        assert resources.requests is not None, "Missing resources.requests in Pod."
        assert resources.requests["cpu"] == "500m", "Incorrect CPU request in Pod resources."
        assert resources.requests["memory"] == "1Gi", "Incorrect memory request in Pod resources."
        assert resources.limits is not None, "Missing resources.limits in Pod."
        assert resources.limits["cpu"] == "1", "Incorrect CPU limit in Pod resources."
        assert resources.limits["memory"] == "2Gi", "Incorrect memory limit in Pod resources."

        logging.info(f"Pod '{pod_name}' in Namespace '{namespace}' has the correct resource requests and limits.")

    def test_002_check_pod_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_pod_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get pod resource-pod -n one -o json"
        result = run_kubectl_command(kube_config, command)
        pod = json.loads(result)

        # 验证Pod的内容
        assert pod["apiVersion"] == "v1", "Incorrect apiVersion."
        assert pod["kind"] == "Pod", "Incorrect kind."
        assert pod["metadata"]["name"] == "resource-pod", "Incorrect metadata.name."
        assert pod["metadata"]["namespace"] == "one", "Incorrect metadata.namespace."

        # 检查Pod的资源请求和限制
        container = pod["spec"]["containers"][0]
        resources = container["resources"]
        assert resources["requests"] is not None, "Missing resources.requests in Pod."
        assert resources["requests"]["cpu"] == "500m", "Incorrect CPU request in Pod resources."
        assert resources["requests"]["memory"] == "1Gi", "Incorrect memory request in Pod resources."
        assert resources["limits"] is not None, "Missing resources.limits in Pod."
        assert resources["limits"]["cpu"] == "1", "Incorrect CPU limit in Pod resources."
        assert resources["limits"]["memory"] == "2Gi", "Incorrect memory limit in Pod resources."

        logging.info(f"Pod 'resource-pod' in Namespace 'one' has the correct resource requests and limits.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
