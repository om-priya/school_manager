from src.utils.hash_password import hash_password


def test_valid_hash_password():
    # setup
    password = "Ompriya@123"
    actual_result = hash_password(password)
    expected_result = "7950ec922ebc6bec22c8b2d545b47debcdb58676ff4a1ed1b80ab06b81e38a1b"

    assert actual_result == expected_result


def test_empty_password_for_haslib():
    password = ""
    actual_result = hash_password(password)
    expected_result = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    assert actual_result == expected_result
