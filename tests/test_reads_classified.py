import os

import pytest
import click

from metagenscope_cli.tools.reads_classified import reads_classified_data, VIRUS_KEY, \
    ARCHAEA_KEY, BACTERIA_KEY, HOST_KEY, UNKNOWN_KEY


@pytest.fixture
def reads_classified_file():
    filename = os.path.join(os.path.dirname(__file__), 'results/reads_classified.json')
    return open(filename)


@pytest.fixture
def reads_classified_missing_host_file():
    filename = os.path.join(os.path.dirname(__file__), 'results/reads_classified_missing_host.json')
    return open(filename)


def test_reads_classified(reads_classified_file):
    data = reads_classified_data(reads_classified_file)
    assert data[VIRUS_KEY] == pytest.approx(0.022771162332126567)
    assert data[ARCHAEA_KEY] == pytest.approx(0.001409979091772543)
    assert data[BACTERIA_KEY] == pytest.approx(89.30381048612026)
    assert data[HOST_KEY] == pytest.approx(0.2352021372463073)
    assert data[UNKNOWN_KEY] == pytest.approx(10.43680623520954)


@pytest.mark.xfail(raises=click.ClickException)
def test_missing_ags(reads_classified_missing_host_file):
    """Ensure error is thrown if required field is missing."""
    data = reads_classified_data(reads_classified_missing_host_file)
