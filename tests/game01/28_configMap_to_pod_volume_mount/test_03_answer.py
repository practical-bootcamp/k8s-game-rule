from tests.helper.test_helper import deploy_answer
import logging


def test_answer(json_input):
    logging.info("Deploying answer with json_input: %s", json_input)
    deploy_answer(json_input)
    logging.info("Answer deployment complete")
