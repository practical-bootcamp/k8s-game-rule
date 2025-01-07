import logging

import pytest
from kubectrl_helper import build_kube_config, run_kubectl_command
from check.game01.test_02_create_namespace import Test02CreateNamespace
from setup.game01.test_02_create_namespace import Test02CreateNamespaceSetup
from cleanup.game01.test_02_create_namespace import Test02CreateNamespaceCleanup
import os


class Test02CreateNamespaceSolution(Test02CreateNamespaceSetup, Test02CreateNamespace, Test02CreateNamespaceCleanup):

    @pytest.mark.order(1)
    def test_000_answer(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"])

        current_folder = os.path.dirname(__file__)
        template_path = os.path.join(
            current_folder, 'test_02_create_namespace.template.yaml')
        yaml_path = os.path.join(
            current_folder, 'test_02_create_namespace.gen.yaml')

        with open(template_path, 'r', encoding='utf-8') as file:
            yaml_content = file.read()
            yaml_content = yaml_content.replace(
                "{namespace}", json_input["namespace"])
            with open(yaml_path, 'w', encoding='utf-8') as file:
                file.write(yaml_content)

        command = f'kubectl apply -f {yaml_path}'
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
