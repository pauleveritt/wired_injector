from wired_injector import hello


def test_hello():
    result: str = hello('World')
    assert result == 'Hello World'
