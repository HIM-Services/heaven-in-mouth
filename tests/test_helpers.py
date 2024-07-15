import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask_app')))

from helpers import validate_email, validate_phone


def test_validate_email():
    assert validate_email('testmail@testdomain.com')
    assert not validate_email('testmail@testdomain')
    assert not validate_email('testmailtestdomain.com')
    assert not validate_email('testmail@testdomain.')
    assert not validate_email('testmail')
    assert not validate_email('^testmail@testdomain.com')
    assert not validate_email('')


def test_validate_phone_number():
    assert validate_phone('123456789')
    assert validate_phone('1234567890')
    assert not validate_phone('1234')
    assert not validate_phone('12345678901')
    assert not validate_phone('12345678a')
    assert not validate_phone('test')


if __name__ == '__main__':
    pytest.main()

# pytest test_helpers.py