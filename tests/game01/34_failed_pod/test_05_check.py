import json
import logging

from kubernetes.client.rest import ApiException

from tests.helper.k8s_client_helper import configure_k8s_client


class TestCheck:
    def test_001_check_pod_absence(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_name = "fail-pod"
        namespace = "one"

        try:
            k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            # 如果Pod存在，则抛出错误
            assert False, f"Pod '{pod_name}' should not have been created."
        except ApiException as e:
            if e.status == 404:
                logging.info(f"Pod '{pod_name}' does not exist as expected.")
            else:
                raise e


# 运行测试
if __name__ == "__main__":
    pytest.main()
