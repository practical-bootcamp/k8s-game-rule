import logging

import pytest

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    @pytest.mark.order(6)
    def test_cleanup(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        # 删除 Pod 而不是命名空间
        command = f"kubectl delete pod nginx -n default"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
