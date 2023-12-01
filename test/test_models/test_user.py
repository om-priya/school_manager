from src.models.users import User
import pytest


@pytest.mark.parametrize(
    "my_class", [User("om", "m", "op@gmail.com", "1221212121", "dav public school")]
)
def test_user_init(my_class):
    assert my_class is not None
