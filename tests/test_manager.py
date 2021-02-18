import pytest
from peewee import DoesNotExist, OperationalError, IntegrityError

from ct8_refresh.account.manager import catcher, require_account


def param_mirror(*args, **kwargs):  # No idea how to name this
    return {'args': args, 'kwargs': kwargs}


def raiser(exception):
    raise exception


def test_catcher_args_kwargs():
    args = {'args': ('foo', 'bar'), 'kwargs': {'spam': 'eggs'}}
    val = catcher()(param_mirror)(*args['args'], **args['kwargs'])
    assert args == val


@pytest.mark.parametrize(
    'exception, operation',
    [
        (DoesNotExist, 'DoesNotExist'),
        (OperationalError, 'OperationalError'),
        (IntegrityError, 'IntegrityError'),
    ],
)
def test_catcher_exceptions(capsys, exception, operation):
    decorated_raiser = catcher(operation)(raiser)
    decorated_raiser(exception)

    out, err = capsys.readouterr()
    assert operation in out


def test_require_account(capsys):
    decorated_raiser = require_account(raiser)
    decorated_raiser(DoesNotExist)

    out, err = capsys.readouterr()
    assert 'does not exists.' in out
