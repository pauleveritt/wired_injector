from wired_injector.utils import caller_package, caller_module


def test_caller_package():
    result = caller_package()
    assert '_pytest' == result.__name__


def test_caller_module():
    result = caller_module()
    assert '_pytest.python' == result.__name__
