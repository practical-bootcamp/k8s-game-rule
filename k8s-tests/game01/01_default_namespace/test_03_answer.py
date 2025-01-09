import pytest


@pytest.mark.order(3)
class TestAnswer:

    @pytest.mark.order(1)
    def test_answer(self, json_input):
        pass
