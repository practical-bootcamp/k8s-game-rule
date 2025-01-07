import logging

import pytest
from kubectrl_helper import build_kube_config, run_kubectl_command


class Test02CreateNamespaceCleanup:

    @pytest.mark.order(99)
    def test_999_cleanup(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"])
        namespace = json_input["namespace"]
        command = f'kubectl delete namespace {namespace}'
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
