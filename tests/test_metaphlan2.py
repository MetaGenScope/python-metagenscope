import os

import pytest
import click

from metagenscope_cli.tools.metaphlan2 import metaphlan2_data


@pytest.fixture
def metaphlan_file():
    filename = os.path.join(os.path.dirname(__file__), 'results/metaphlan2.tsv')
    return open(filename)


def test_metaphlan2(metaphlan_file):
    data = metaphlan2_data(metaphlan_file, '#SampleID', 'Metaphlan2_Analysis')
    assert data[0]['taxon'] == 'k__Bacteria'
    assert data[0]['abundance'] == pytest.approx(95.88884)
    assert data[1]['taxon'] == 'k__Viruses'
    assert data[1]['abundance'] == pytest.approx(4.11116)
    assert data[2]['taxon'] == 'k__Bacteria|p__Firmicutes'
    assert data[2]['abundance'] == pytest.approx(60.16273)
    assert data[3]['taxon'] == 'k__Bacteria|p__Actinobacteria'
    assert data[3]['abundance'] == pytest.approx(24.6525)
    assert data[4]['taxon'] == 'k__Bacteria|p__Proteobacteria'
    assert data[4]['abundance'] == pytest.approx(11.07361)


@pytest.mark.xfail(raises=click.ClickException)
def test_incorrect_taxon_name(metaphlan_file):
    data = metaphlan2_data(metaphlan_file, 'BadName', 'Metaphlan2_Analysis')


@pytest.mark.xfail(raises=click.ClickException)
def test_incorrect_taxon_name(metaphlan_file):
    data = metaphlan2_data(metaphlan_file, '#SampleID', 'BadName')
