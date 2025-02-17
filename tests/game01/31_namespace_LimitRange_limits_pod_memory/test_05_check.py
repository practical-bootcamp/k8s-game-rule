import json
import logging

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCheck:
    def test_001_check_limitrange_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace = json_input["namespace"]
        limitrange_name = "mem-limit-range"

        # 验证 LimitRange
        try:
            logging.info("Checking LimitRange '%s' in namespace '%s' using client", limitrange_name, namespace)
            limitrange = k8s_client.read_namespaced_limit_range(name=limitrange_name, namespace=namespace)
        except Exception as e:
            logging.error("Failed to get LimitRange '%s': %s", limitrange_name, str(e))
            assert False, f"Failed to get LimitRange '{limitrange_name}': {str(e)}"

        # 验证 LimitRange 中的内存限制
        limits = limitrange.spec.limits[0]
        max_memory = limits.max["memory"]
        min_memory = limits.min["memory"]
        assert max_memory == "500Mi", f"Expected max memory to be '500Mi', but got '{max_memory}'."
        assert min_memory == "100Mi", f"Expected min memory to be '100Mi', but got '{min_memory}'."
        logging.info("LimitRange '%s' has the correct memory limits: max='500Mi', min='100Mi'.", limitrange_name)

    def test_002_check_limitrange_kubectl(self, json_input):
        logging.debug("Starting test_002_check_limitrange_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        namespace = json_input["namespace"]
        limitrange_name = "mem-limit-range"

        # 使用 kubectl 获取 LimitRange
        command = f"kubectl get limitrange {limitrange_name} -n {namespace} -o json"
        result = run_kubectl_command(kube_config, command)

        # 解析 kubectl 输出的 JSON 内容
        limitrange = json.loads(result)

        # 验证 LimitRange 的内容
        assert limitrange["apiVersion"] == "v1", "Incorrect apiVersion."
        assert limitrange["kind"] == "LimitRange", "Incorrect kind."
        assert limitrange["metadata"]["name"] == limitrange_name, "Incorrect metadata.name."

        # 验证 LimitRange 中的内存限制
        limits = limitrange["spec"]["limits"][0]
        max_memory = limits["max"]["memory"]
        min_memory = limits["min"]["memory"]
        assert max_memory == "500Mi", f"Expected max memory to be '500Mi', but got '{max_memory}'."
        assert min_memory == "100Mi", f"Expected min memory to be '100Mi', but got '{min_memory}'."
        logging.info("LimitRange '%s' has the correct memory limits: max='500Mi', min='100Mi'.", limitrange_name)
