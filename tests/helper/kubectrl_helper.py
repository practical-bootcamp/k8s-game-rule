import base64
import json
import logging
import os
import subprocess
import tempfile


def build_kube_config(client_certificate, client_key, endpoint):
    cert_data = base64.b64encode(client_certificate.encode("utf-8")).decode("utf-8")
    key_data = base64.b64encode(client_key.encode("utf-8")).decode("utf-8")

    return {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [{"name": "k8s-cluster", "cluster": {"server": endpoint}}],
        "contexts": [
            {
                "name": "k8s-context",
                "context": {"cluster": "k8s-cluster", "user": "k8s-user"},
            }
        ],
        "current-context": "k8s-context",
        "users": [
            {
                "name": "k8s-user",
                "user": {
                    "client-certificate-data": cert_data,
                    "client-key-data": key_data,
                },
            }
        ],
    }


def run_kubectl_command(kube_config, command):
    with tempfile.NamedTemporaryFile(delete=False) as temp_config:
        temp_config.write(json.dumps(kube_config).encode())
        temp_config.flush()
        os.environ["KUBECONFIG"] = temp_config.name
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
    return result.stdout


def delete_namespace(json_input):
    kube_config = build_kube_config(
        json_input["cert_file"], json_input["key_file"], json_input["host"]
    )

    pod_namespace = json_input["namespace"]
    command = f"kubectl delete namespace  {pod_namespace}"
    result = run_kubectl_command(kube_config, command)
    logging.info(result)
