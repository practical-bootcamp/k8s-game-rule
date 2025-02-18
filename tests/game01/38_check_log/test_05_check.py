import json
import logging
import time

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

class TestCheck:
    def test_001_check_pod_creation(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace = json_input["namespace"]
        pod_name = "busybox-pod"
        container_name = "busybox"

        logging.info(f"Using namespace: {namespace}")
        logging.info(f"Checking if Pod '{pod_name}' is created in namespace '{namespace}' using client")

        # 验证 Pod 是否成功创建
        try:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            assert pod is not None, f"Pod '{pod_name}' not found in namespace '{namespace}'"
            logging.info(f"Pod '{pod_name}' found in namespace '{namespace}'")
        except Exception as e:
            logging.error(f"Failed to get Pod '{pod_name}': {str(e)}")
            assert False, f"Failed to get Pod '{pod_name}': {str(e)}"

    def test_002_check_pod_logs(self, json_input):
        logging.debug("Starting test_002_check_pod_logs")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        namespace = json_input["namespace"]
        pod_name = "busybox-pod"
        container_name = "busybox"

        logging.info(f"Using namespace: {namespace}")
        logging.info(f"Checking logs for Pod '{pod_name}' in namespace '{namespace}' using kubectl")

        # 等待 Pod 完全启动
        time.sleep(7)

        # 使用 kubectl 获取 Pod 日志
        command = f"kubectl logs {pod_name} -n {namespace} --tail=10"
        result = run_kubectl_command(kube_config, command)

        # 检查日志输出
        logs = result
        logging.info(f"Logs for Pod '{pod_name}':\n{logs}")
        assert "0: " in logs, "Expected log output not found."
