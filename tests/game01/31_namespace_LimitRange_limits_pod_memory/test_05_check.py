import json
import logging

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCheck:
    def test_001_check_namespace(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace_name = "limitrange"

        try:
            namespace = k8s_client.read_namespace(name=namespace_name)
        except Exception as e:
            assert False, f"Failed to get Namespace '{namespace_name}': {str(e)}"

        # 验证Namespace的内容
        assert namespace.metadata.name == namespace_name, "Incorrect metadata.name."
        logging.info(f"Namespace '{namespace_name}' exists.")

    def test_002_check_limitrange(self, json_input):
        logging.debug("Starting test_002_check_limitrange")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get limitrange mem-limit-range -n limitrange -o json"
        result = run_kubectl_command(kube_config, command)
        limitrange = json.loads(result)

        # 验证LimitRange的内容
        assert limitrange["apiVersion"] == "v1", "Incorrect apiVersion."
        assert limitrange["kind"] == "LimitRange", "Incorrect kind."
        assert (
            limitrange["metadata"]["name"] == "mem-limit-range"
        ), "Incorrect metadata.name."
        assert (
            limitrange["metadata"]["namespace"] == "limitrange"
        ), "Incorrect metadata.namespace."
        limits = limitrange["spec"]["limits"][0]
        assert limits["max"]["memory"] == "500Mi", "Incorrect max memory limit."
        assert limits["min"]["memory"] == "100Mi", "Incorrect min memory limit."
        assert limits["type"] == "Pod", "Incorrect limit type."

        logging.info(
            f"LimitRange 'mem-limit-range' in Namespace 'limitrange' has the correct memory limits."
        )


# 运行测试
if __name__ == "__main__":
    pytest.main()
