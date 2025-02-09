import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_pod_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_name = "fail-pod"
        namespace = "one"

        try:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
        except Exception as e:
            logging.info(f"Pod '{pod_name}' was not created as expected due to ResourceQuota violation.")
            return

        # 如果Pod被创建，则抛出错误
        assert False, f"Pod '{pod_name}' should not have been created due to ResourceQuota violation."

    def test_002_check_pod_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_pod_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get pod fail-pod -n one -o json"
        result = run_kubectl_command(kube_config, command)

        # 如果命令返回非空结果，则Pod存在，这会抛出错误
        if result:
            pod = json.loads(result)
            if pod:
                assert False, f"Pod 'fail-pod' should not have been created due to ResourceQuota violation."

        logging.info(f"Pod 'fail-pod' was not created as expected due to ResourceQuota violation.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
