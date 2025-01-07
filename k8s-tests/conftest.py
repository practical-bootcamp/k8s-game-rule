import json
import os
import pytest
import logging
from names_generator import generate_name


@pytest.fixture(scope='module', autouse=True)
def json_input(request):
    # for local testing
    if not os.path.exists("/tmp/json_input.json"):
        with open('/workspaces/k8s-game-rule/k8s-configure/endpoint.txt', 'r', encoding='utf-8') as endpoint_file:
            host = endpoint_file.read().strip()
        result = {
            "cert_file": '/workspaces/k8s-game-rule/k8s-configure/client.crt',
            "key_file": '/workspaces/k8s-game-rule/k8s-configure/client.key',
            "host": host
        }
        test_path_name = request.path
        folder_path = os.path.dirname(test_path_name)
        folder_path = folder_path.replace("/rules/", "/setup/")
        folder_path = folder_path.replace("/cleanup/", "/setup/")
        folder_path = folder_path.replace("/answers/", "/setup/")
        session_json_file = os.path.join(folder_path, "session.json")

        if os.path.exists(session_json_file):
            with open(session_json_file, 'r', encoding="utf-8") as file:
                session_json = json.load(file)
                random_name = generate_name().replace("_", "")
                student_id = "123456789"
                for key, value in session_json.items():
                    if isinstance(value, str):
                        session_json[key] = value \
                            .replace("{random_name}", random_name) \
                            .replace("{student_id}", student_id)
                logging.info(session_json)
            result.update(session_json)
        return result
    # for running in AWS lambda
    with open("/tmp/json_input.json", 'r', encoding="utf-8") as file:
        json_str_input = file.read()
        result = json.loads(json_str_input)
    return result
