from tests.helper.kubectrl_helper import delete_namespace


class TestCleanup:
    def test_cleanup(self, json_input):
        delete_namespace(json_input)
