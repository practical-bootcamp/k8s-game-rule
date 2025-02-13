import logging

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    def test_cleanup(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        namespace = json_input["namespace"]
        command = f"kubectl delete namespace {namespace}"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
