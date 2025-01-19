import logging
import os

import pytest

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


@pytest.mark.order(3)
def test_answer(json_input):
    kube_config = build_kube_config(
        json_input["cert_file"], json_input["key_file"], json_input["host"]
    )

    current_folder = os.path.dirname(__file__)
    template_path = os.path.join(current_folder, "answer.template.yaml")
    yaml_path = os.path.join(current_folder, "answer.gen.yaml")

    with open(template_path, "r", encoding="utf-8") as file:
        yaml_content = file.read()
        with open(yaml_path, "w", encoding="utf-8") as file:
            file.write(yaml_content)

    command = f"kubectl apply -f {yaml_path}"
    result = run_kubectl_command(kube_config, command)
    logging.info(result)
    assert "pod/nginx created" in result, "Pod 'nginx' was not created"
