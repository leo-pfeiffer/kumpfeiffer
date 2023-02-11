import pytest
import logging

from kumpfeiffer.settings import BASE_DIR

logging.disable(logging.CRITICAL)


@pytest.fixture
def guests_csv():
    return BASE_DIR / "wedding/test/test_resources/guests.csv"
