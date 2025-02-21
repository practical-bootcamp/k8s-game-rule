import logging

from tests.helper.k8s_client_helper import configure_k8s_client


class TestCheck:
    def test_001_check_resourcequota_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace = json_input["namespace"]
        resourcequota_name = "resource-quota"

        # 验证 ResourceQuota
        try:
            logging.info(
                "Checking ResourceQuota '%s' in namespace '%s' using client",
                resourcequota_name,
                namespace,
            )
            resourcequota = k8s_client.read_namespaced_resource_quota(
                name=resourcequota_name, namespace=namespace
            )
        except Exception as e:
            logging.error(
                "Failed to get ResourceQuota '%s': %s", resourcequota_name, str(e)
            )
            assert (
                False
            ), f"Failed to get ResourceQuota '{resourcequota_name}': {str(e)}"

        # 验证 ResourceQuota 中的硬性限制
        hard = resourcequota.spec.hard
        assert (
            hard["requests.cpu"] == "1"
        ), f"Expected requests.cpu to be '1', but got '{hard['requests.cpu']}'."
        assert (
            hard["requests.memory"] == "1Gi"
        ), f"Expected requests.memory to be '1Gi', but got '{hard['requests.memory']}'."
        assert (
            hard["limits.cpu"] == "2"
        ), f"Expected limits.cpu to be '2', but got '{hard['limits.cpu']}'."
        assert (
            hard["limits.memory"] == "2Gi"
        ), f"Expected limits.memory to be '2Gi', but got '{hard['limits.memory']}'."
        logging.info(
            "ResourceQuota '%s' has the correct hard limits.", resourcequota_name
        )

    def test_002_check_pod_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace = json_input["namespace"]
        pod_name = "resource-pod"

        # 验证 Pod
        try:
            logging.info(
                "Checking Pod '%s' in namespace '%s' using client", pod_name, namespace
            )
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
        except Exception as e:
            logging.error("Failed to get Pod '%s': %s", pod_name, str(e))
            assert False, f"Failed to get Pod '{pod_name}': {str(e)}"

        # 验证 Pod 中的资源请求和限制
        resources = pod.spec.containers[0].resources
        cpu_request = resources.requests["cpu"]
        memory_request = resources.requests["memory"]
        cpu_limit = resources.limits["cpu"]
        memory_limit = resources.limits["memory"]

        assert cpu_request in [
            "0.5",
            "500m",
        ], f"Expected requests.cpu to be '0.5' or '500m', but got '{cpu_request}'."
        assert (
            memory_request == "1Gi"
        ), f"Expected requests.memory to be '1Gi', but got '{memory_request}'."
        assert (
            cpu_limit == "1"
        ), f"Expected limits.cpu to be '1', but got '{cpu_limit}'."
        assert (
            memory_limit == "2Gi"
        ), f"Expected limits.memory to be '2Gi', but got '{memory_limit}'."

        logging.info("Pod '%s' has the correct resource requests and limits.", pod_name)
