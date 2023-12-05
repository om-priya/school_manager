import pytest
from src.utils.pretty_print import pretty_print


class TestPrettyPrint:
    valid_input_data = [
        ([(1, "Om Priya"), (2, "Shreyansh")], ("Id", "Name")),
    ]

    invalid_input_data = [
        ([(1, "Om Priya"), (2, "Shreyansh")], None),
        ({1: "Om Priya", 2: "Shreyansh"}),
    ]


    @pytest.mark.parametrize("res_data, headers", valid_input_data)
    def test_pretty_print_valid_input(self, res_data, headers):
        pretty_print(res_data, headers)


    @pytest.mark.parametrize("res_data, headers", invalid_input_data)
    def test_pretty_print_invalid_input(self, res_data, headers):
        with pytest.raises(Exception):
            pretty_print(res_data, headers)
