import pytest

from tests.helper.test_helper import deploy_setup


@pytest.mark.order(1)
def test_setup(json_input):
    deploy_setup(json_input)
