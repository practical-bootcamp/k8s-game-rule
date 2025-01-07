import logging

import pytest
from kubectrl_helper import build_kube_config, run_kubectl_command
from rules.game01.test_02_create_namespace import Test02CreateNamespace
from setup.game01.test_02_create_namespace import Test02CreateNamespaceSetup
from cleanup.game01.test_02_create_namespace import Test02CreateNamespaceCleanup


class Test02CreateNamespaceSolution(Test02CreateNamespaceSetup, Test02CreateNamespace, Test02CreateNamespaceCleanup):

    @pytest.mark.order(1)
    def test_000_answer(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"])
        namespace = json_input["namespace"]
        command = f'kubectl create namespace {namespace}'
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
