from unittest import mock

import pytest

from repoze import tm as repoze_tm


class LocalTestError(ValueError):
    def __init__(self):
        super().__init__("local test error")


@pytest.fixture
def transaction_module():
    with mock.patch("repoze.tm.transaction", DummyTransactionModule()) as txn:
        yield txn


@pytest.fixture
def app():
    return DummyApplication()


@pytest.fixture
def start_response():

    def _start_response(status, headers, exc_info=None):  # pragma: NO COVER
        pass

    return mock.create_autospec(_start_response, return_value=["hello"])


def test_tm_ekey_inserted(transaction_module, app, start_response):
    tm = repoze_tm.TM(app)
    env = {}

    result = [chunk for chunk in tm(env, start_response)]

    assert result == start_response.return_value
    assert repoze_tm.ekey in env


def test_tm_committed(transaction_module, app, start_response):
    tm = repoze_tm.TM(app)

    result = [chunk for chunk in tm({}, start_response)]

    assert result == start_response.return_value
    assert transaction_module.committed
    assert not transaction_module.aborted


def test_tm_aborted_via_doom(transaction_module, app, start_response):
    transaction_module.doom = True

    tm = repoze_tm.TM(app)

    result = [chunk for chunk in tm({}, start_response)]

    assert result == start_response.return_value
    assert not transaction_module.committed
    assert transaction_module.aborted


def test_tm_aborted_via_exception(transaction_module, app, start_response):
    app.exception = True

    tm = repoze_tm.TM(app)

    def execute_request():
        [chunk for chunk in tm({}, start_response)]

    with pytest.raises(LocalTestError):
        execute_request()

    assert not transaction_module.committed
    assert transaction_module.aborted


def test_tm_aborted_via_exception_and_doom(
    transaction_module,
    app,
    start_response,
):
    transaction_module.doom = True
    app.exception = True

    tm = repoze_tm.TM(app)

    def execute_request():
        [chunk for chunk in tm({}, start_response)]

    with pytest.raises(LocalTestError):
        execute_request()

    assert not transaction_module.committed
    assert transaction_module.aborted


def test_tm_aborted_via_commit_veto(transaction_module, app, start_response):
    app.status = "403 Forbidden"

    def commit_veto(environ, status, headers):
        assert isinstance(environ, dict)
        assert isinstance(headers, list)
        assert isinstance(status, str)
        status_code = int(status.split()[0])
        return not (200 <= status_code < 400)

    tm = repoze_tm.TM(app, commit_veto)

    [chunk for chunk in tm({}, start_response)]

    assert not transaction_module.committed
    assert transaction_module.aborted


def test_tm_committed_via_commit_veto_exception(
    transaction_module,
    app,
    start_response,
):
    app.status = "403 Forbidden"

    def commit_veto(environ, status, headers):
        return None

    tm = repoze_tm.TM(app, commit_veto)

    [chunk for chunk in tm({}, start_response)]

    assert transaction_module.committed
    assert not transaction_module.aborted


def test_tm_aborted_via_commit_veto_exception(
    transaction_module,
    app,
    start_response,
):
    app.status = "403 Forbidden"

    def commit_veto(environ, status, headers):
        raise LocalTestError()

    tm = repoze_tm.TM(app, commit_veto)

    def execute_request():
        [chunk for chunk in tm({}, start_response)]

    with pytest.raises(LocalTestError):
        execute_request()

    assert not transaction_module.committed
    assert transaction_module.aborted


def test_tm_cleanup_on_commit(transaction_module, app, start_response):
    env = {}
    dummy = mock.Mock(spec_set=())
    setattr(transaction_module, repoze_tm.after_end.key, [dummy])

    tm = repoze_tm.TM(app)

    [chunk for chunk in tm(env, start_response)]

    assert transaction_module.committed
    assert not transaction_module.aborted
    dummy.assert_called_once_with()


def test_tm_cleanup_on_abort(transaction_module, app, start_response):
    app.exception = True
    env = {}
    dummy = mock.Mock(spec_set=())
    setattr(transaction_module, repoze_tm.after_end.key, [dummy])

    tm = repoze_tm.TM(app)

    def execute_request():
        [chunk for chunk in tm(env, start_response)]

    with pytest.raises(LocalTestError):
        execute_request()

    assert not transaction_module.committed
    assert transaction_module.aborted
    dummy.assert_called_once_with()


def any_args(*args):  # pragma: NO COVER
    return None


@pytest.fixture
def txn():
    key = repoze_tm.AfterEnd.key
    return mock.Mock(spec_set=[key], **{key: None})


def test_afterend_register_wo_funcs(txn):
    registry = repoze_tm.AfterEnd()
    registry.register(any_args, txn)

    assert getattr(txn, registry.key) == [any_args]


def test_afterend_register_w_funcs(txn):
    funcs = []
    setattr(txn, repoze_tm.AfterEnd.key, funcs)
    registry = repoze_tm.AfterEnd()

    registry.register(any_args, txn)

    assert funcs == [any_args]


def test_afterend_unregister_exists(txn):
    registry = repoze_tm.AfterEnd()
    registry.register(any_args, txn)

    assert getattr(txn, registry.key) == [any_args]

    registry.unregister(any_args, txn)

    assert not hasattr(txn, registry.key)


def test_afterend_unregister_not_exists(txn):
    registry = repoze_tm.AfterEnd()
    setattr(txn, registry.key, [None])

    registry.unregister(any_args, txn)

    assert getattr(txn, registry.key) == [None]


def test_afterend_unregister_funcs_is_None(txn):
    registry = repoze_tm.AfterEnd()

    assert registry.unregister(any_args, txn) is None


def test_isActive_w_ekey():
    assert repoze_tm.isActive({repoze_tm.ekey: True})


def test_isActive_wo_ekey():
    assert not repoze_tm.isActive({})


def test_make_tm_withveto(app):
    from tests.unit.util import fakeveto

    tm = repoze_tm.make_tm(app, {}, "tests.unit.util:fakeveto")
    assert tm.commit_veto == fakeveto


def test_make_tm_noveto(app):
    tm = repoze_tm.make_tm(app, {}, None)
    assert tm.commit_veto is None


@pytest.mark.parametrize(
    "status",
    [
        "500 Server Error",
        "503 Service Unavailable",
        "400 Bad Request",
        "411 Length Required",
    ],
)
def test_default_commit_veto_no_headers_w_error(status):
    assert repoze_tm.default_commit_veto(None, status, ())


@pytest.mark.parametrize(
    "status",
    [
        "200 OK",
        "201 Created",
        "301 Moved Permanently",
        "302 Found",
    ],
)
def test_default_commit_veto_no_headers_wo_error(status):
    assert not repoze_tm.default_commit_veto(None, status, ())


@pytest.mark.parametrize(
    "headers",
    [
        [("X-Tm-Abort", True)],
        [("X-Tm", "abort")],
        [("X-Tm", "")],
    ],
)
def test_default_commit_veto_true_w_w_x_tm_headers(headers):
    assert repoze_tm.default_commit_veto(None, "200 OK", headers)


@pytest.mark.parametrize(
    "headers",
    [[("X-Tm", "commit")], [("X-Tm", "commit"), ("X-Tm-Abort", True)]],
)
def test_default_commit_veto_false_w_w_x_tm_headers(headers):
    assert not repoze_tm.default_commit_veto(None, "200 OK", headers)


def test_default_commit_veto_false_w_other_headers():
    headers = [("X-Other", "test")]
    assert not repoze_tm.default_commit_veto(None, "200 OK", headers)


class DummyTransactionModule:
    begun = False
    committed = False
    aborted = False
    doom = False

    def begin(self):
        self.begun = True

    def get(self):
        return self

    def commit(self):
        self.committed = True

    def abort(self):
        self.aborted = True

    def isDoomed(self):
        return self.doom


class DummyApplication:
    def __init__(self, exception=False, status="200 OK"):
        self.exception = exception
        self.status = status

    def __call__(self, environ, start_response):
        result = start_response(self.status, [], None)

        if self.exception:
            raise LocalTestError()

        return result
