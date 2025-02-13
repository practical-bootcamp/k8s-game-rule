import logging

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCheck:

    def test_001_namespace_exists_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        namespace = json_input["namespace"]
        namespaces = k8s_client.list_namespace()
        namespace_names = [ns.metadata.name for ns in namespaces.items]
        assert namespace in namespace_names, f"Namespace '{namespace}' does not exist"

    def test_002_namespace_exists_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        command = "kubectl get namespace"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
        namespace = json_input["namespace"]
        assert namespace in result, f"Namespace '{namespace}' does not exist"
