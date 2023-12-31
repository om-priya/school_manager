import builtins
from src.utils.validate import (
    validator,
    pattern_validator,
    uuid_validator,
    password_validator,
    validate_date,
)
from src.config.regex_pattern import RegexPatterns
import pytest
from datetime import datetime, timedelta

class TestValidate:
    valid_input_data = [
    (RegexPatterns.UUID_PATTERN, "123ASd"),
    (RegexPatterns.PASSWORD_PATTERN, "Ompriya@123"),
    (RegexPatterns.NAME_PATTERN, "Om Priya"),
    (RegexPatterns.USERNAME_PATTERN, "ompriya18"),
    (RegexPatterns.EMAIL_PATTERN, "ompriya18153789@gmail.com"),
    (RegexPatterns.ROLE_PATTERN, "teacher"),
    (RegexPatterns.GENDER_PATTERN, "m"),
    (RegexPatterns.DATE_PATTERN, "12-12-2002"),
    (RegexPatterns.DAYS_PATTERN, "12"),
    (RegexPatterns.MESSAGE_PATTERN, "djhjhjdn donjdnocn owdnjdnjc"),
    (RegexPatterns.FAV_SUBJECT_PATTERN, "dfndjnc uiedjb"),
    (RegexPatterns.PHONE_PATTERN, "8229070126"),
    (RegexPatterns.EXPERIENCE_PATTERN, "9"),
    ]

    invalid_input_data = [
        (RegexPatterns.UUID_PATTERN, "123d"),
        (RegexPatterns.PASSWORD_PATTERN, "ompriya23"),
        (RegexPatterns.NAME_PATTERN, "Om123 Priya"),
        (RegexPatterns.USERNAME_PATTERN, "ompriya18@"),
        (RegexPatterns.EMAIL_PATTERN, "ompr@iya18153789@gmail.com"),
        (RegexPatterns.ROLE_PATTERN, "superman"),
        (RegexPatterns.GENDER_PATTERN, "M"),
        (RegexPatterns.DATE_PATTERN, "12-1212-2002"),
        (RegexPatterns.DAYS_PATTERN, "1212121"),
        (RegexPatterns.MESSAGE_PATTERN, ""),
        (RegexPatterns.FAV_SUBJECT_PATTERN, "dfndjnc2121 uiedjb"),
        (RegexPatterns.PHONE_PATTERN, "82290701261"),
        (RegexPatterns.EXPERIENCE_PATTERN, "912121"),
    ]
    # testing for validator and invalid data
    @pytest.mark.parametrize("pattern, input_data", valid_input_data)
    def test_valid_input(self, pattern, input_data):
        assert validator(pattern, input_data)


    @pytest.mark.parametrize("pattern, input_data", invalid_input_data)
    def test_invalid_input(self, pattern, input_data):
        assert not validator(pattern, input_data)


    # testing for pattern_validator function
    def test_pattern_validator(self, monkeypatch):
        # setup var
        prompt = ""
        pattern = RegexPatterns.NAME_PATTERN
        test_data_for_input = ["", "1234w", "om1 priya", "om priya"]

        monkeypatch.setattr(builtins, "input", lambda _: test_data_for_input.pop(0))

        expected_result = pattern_validator(prompt, pattern)

        assert expected_result == "om priya"


    # testing for uuid_validator function
    def test_uuid_validator(self, monkeypatch):
        # setup var
        prompt = ""
        pattern = RegexPatterns.UUID_PATTERN
        test_data_for_input = ["", "1234w", "om1 priya", "12ASxw"]

        monkeypatch.setattr(builtins, "input", lambda _: test_data_for_input.pop(0))

        expected_result = uuid_validator(prompt, pattern)

        assert expected_result == "12ASxw"


    # testing for password validator
    def test_password_validator(self, monkeypatch):
        test_data_for_input = ["", "1234w", "om1 priya", "Ompriya@123"]

        monkeypatch.setattr(
            "src.utils.validate.maskpass.advpass",
            lambda **kwargs: test_data_for_input.pop(0),
        )
        expected_result = password_validator()
        assert expected_result == "Ompriya@123"


    def test_validate_date(self, monkeypatch, capsys):
        past_date = (datetime.now() - timedelta(days=7)).strftime("%d-%m-%Y")
        future_date = (datetime.now() + timedelta(days=7)).strftime("%d-%m-%Y")
        options = [past_date, future_date]
        monkeypatch.setattr("builtins.input", lambda _: options.pop(0))

        expected_result = validate_date("")

        captured = capsys.readouterr()

        assert "\nInvalid Input For Date\n" in captured.out
        assert str(expected_result) == (datetime.now() + timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )


    def test_validate_date_invalid_date(self, monkeypatch, capsys):
        invalid_date = "30-02-2023"
        future_date = (datetime.now() + timedelta(days=7)).strftime("%d-%m-%Y")
        options = [invalid_date, future_date]
        monkeypatch.setattr("builtins.input", lambda _: options.pop(0))

        expected_result = validate_date("")

        captured = capsys.readouterr()

        assert "\nInvalid Input For Date\n" in captured.out
        assert str(expected_result) == (datetime.now() + timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )
