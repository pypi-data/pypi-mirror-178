"""Package-wide test fixtures."""
from unittest.mock import Mock

import pytest
from pytest_mock import MockFixture


@pytest.fixture
def mock_toml_loads(mocker: MockFixture) -> Mock:
    """Fixture for mocking tomllib.loads."""
    mock = mocker.patch("tomllib.loads")
    mock.return_value = {
        "circled": dict(
            zip(
                "abcdefghijklmnopqrstuvwxyzDRESSUP", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒹⓇⒺⓈⓈⓊⓅ"
            )
        ),
        "negative_circled": dict(
            zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩")
        ),
    }
    return mock
