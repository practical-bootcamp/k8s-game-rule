# test_06_cleanup.py
import pytest

from tests.helper.kubectrl_helper import delete_namespace


class TestCleanup:

    @pytest.mark.order(6)
    def test_cleanup(self, json_input):
        delete_namespace(json_input)
