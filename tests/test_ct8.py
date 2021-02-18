import uuid

import pytest
import requests_mock as rm_module
from loguru import logger
from pytest_mock import MockerFixture

from ct8_refresh.constants import SIGNIN_URL
from ct8_refresh.ct8 import CT8

logger.remove()


@pytest.fixture
def ct8_account():
    return CT8(username='john', password='password123')


# def test_ct8_login_page_200_response():
#     request = requests.get('https://panel.ct8.pl/login/')
#
#     assert request.status_code == 200
#     assert not len(request.history)  # no redirect has happened


def test_sign_in_request(ct8_account):
    with rm_module.Mocker(session=ct8_account.session) as session_mock:
        session_mock.get(SIGNIN_URL, status_code=200)

        session_mock.post(SIGNIN_URL, status_code=200)
        ct8_account.sign_in_request()
        assert not ct8_account.signed_in

        session_mock.post(SIGNIN_URL, status_code=302)
        ct8_account.sign_in_request()
        assert ct8_account.signed_in


def test_update_expiration_date(ct8_account, mocker: MockerFixture):
    m = mocker.patch(
        'ct8_refresh.account.manager.AccountsManager.update_expiration_date'
    )

    ct8_account.signed_in = True
    ct8_account.update_expiration_date()

    assert m.call_count == 1


def test__prepare_header(ct8_account):
    token = str(uuid.uuid4())
    header = ct8_account._prepare_header(token)
    assert f'csrftoken={token}' in header.values()
