import os

import pytest
import click

from metagenscope_cli.tools.microbe_census import microbe_census_data, AGS_KEY, TOTAL_BASES_KEY, \
    GENOME_EQUIVALENTS_KEY


@pytest.fixture
def microbe_census_file():
    filename = os.path.join(os.path.dirname(__file__), 'results/mic_census')
    return open(filename)


@pytest.fixture
def microbe_census_missing_ags_file():
    filename = os.path.join(os.path.dirname(__file__), 'results/mic_census_missing_ags')
    return open(filename)


def test_microbe_census(microbe_census_file):
    data = microbe_census_data(microbe_census_file)
    assert data[AGS_KEY] == pytest.approx(70513906.6967)
    assert data[TOTAL_BASES_KEY] == 1709470396
    assert data[GENOME_EQUIVALENTS_KEY] == pytest.approx(24.2430249022)


@pytest.mark.xfail(raises=click.ClickException)
def test_missing_ags(microbe_census_missing_ags_file):
    """Ensure error is thrown if required field is missing."""
    data = microbe_census_data(microbe_census_missing_ags_file)
