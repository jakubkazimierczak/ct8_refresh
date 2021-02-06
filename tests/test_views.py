from datetime import datetime, timedelta

import pytest

from ct8_refresh.account.model import Account
from ct8_refresh.account.views import AccountsView


def parse_line(line):
    return [_.strip() for _ in line[1:-2].split('│')]


@pytest.fixture
def accounts(freezer):
    freezer.move_to('2012-02-01 12:00')
    expires_on = [
        datetime.today() + timedelta(days=89),
    ]
    return [
        Account(name='john', is_active=True, expires_on=expires_on[0]),
        Account(name='paul', is_active=False),
    ]


def test_output(capsys, accounts):
    AccountsView.show_accounts(accounts)

    org_out, err = capsys.readouterr()
    out = org_out.split('\n')

    # Check if table contains all columns
    assert 'Users' in out[0]
    header = parse_line(out[2])
    assert header == ['Name', 'Enabled', 'Expires on', 'Remaining days']

    # Check if records are present
    line = parse_line(out[4])
    assert line == ['john', 'True', '2012-04-30 12:00:00', '89']

    line = parse_line(out[5])
    assert line == ['paul', 'False', '', '0']
