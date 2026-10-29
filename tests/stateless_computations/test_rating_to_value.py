import pytest

from e_disclosure._stateless_computations.rating_to_value import rating_to_value


def test_rating_to_value(subtests) -> None:
    cases = {"national": ("ruA-", 17), "bare": ("bbb", 15), "bounds": ("ruAAA", 23)}
    for name, (rating, value) in cases.items():
        with subtests.test(name):
            assert rating_to_value(rating) == value


def test_rating_to_value_unknown() -> None:
    with pytest.raises(ValueError, match="Неизвестный рейтинг"):
        rating_to_value("ruA++")
