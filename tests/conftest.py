from datetime import date, timedelta

import pytest


@pytest.fixture
def today():
    return date.today()


@pytest.fixture
def tomorrow():
    return date.today() + timedelta(1)


@pytest.fixture
def later():
    return date.today() + timedelta(10)
