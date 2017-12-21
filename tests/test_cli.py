import pytest
from click.testing import CliRunner
from metagenscope_cli import hello


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(hello.hello)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Hello, world.'


def test_cli_with_option(runner):
    result = runner.invoke(hello.hello, ['--as-cowboy'])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'Howdy, world.'


def test_cli_with_arg(runner):
    result = runner.invoke(hello.hello, ['Benjamin'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'Hello, Benjamin.'
