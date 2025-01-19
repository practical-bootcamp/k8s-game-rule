import logging

import pytest

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    @pytest.mark.order(6)
    def test_cleanup(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        pod_name = "nginx"
        pod_namespace = "default"
        command = f"kubectl delete pod {pod_name} -n {pod_namespace}"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)