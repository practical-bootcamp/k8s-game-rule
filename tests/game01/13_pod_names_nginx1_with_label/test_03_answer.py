import pytest

from tests.helper.test_helper import deploy_answer


@pytest.mark.order(3)
def test_answer(json_input):
    deploy_answer(json_input)
