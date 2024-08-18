import pytest

from zibal.utils import (
    to_camel_case_dict,
    to_snake_case_dict,
    convert_to_camel_case,
    convert_to_snake_case,
)


@pytest.mark.parametrize(
    "string, expected",
    [
        ("", ""),
        ("word", "word"),
        ("some_string", "someString"),
        ("some_snakes_are_lurking_nearby", "someSnakesAreLurkingNearby"),
    ],
)
def test_to_camel_case_string(string, expected):
    assert convert_to_camel_case(string) == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        ("", ""),
        ("word", "word"),
        ("someString", "some_string"),
        ("thereAreTooManyCamelsHere", "there_are_too_many_camels_here"),
    ],
)
def test_to_snake_case_string(string, expected):
    assert convert_to_snake_case(string) == expected


def test_to_camel_case_dict():
    snake_case_dict = {
        "first_key": 1,
        "second_key": 2,
        "third_key": 3,
    }
    new_dict = to_camel_case_dict(snake_case_dict)
    expected_dict = {"firstKey": 1, "secondKey": 2, "thirdKey": 3}
    assert new_dict == expected_dict


def test_to_snake_case_dict():
    camel_case_dict = {"firstKey": 1, "secondKey": 2, "thirdKey": 3}
    new_dict = to_snake_case_dict(camel_case_dict)
    expected_dict = {
        "first_key": 1,
        "second_key": 2,
        "third_key": 3,
    }
    assert new_dict == expected_dict
