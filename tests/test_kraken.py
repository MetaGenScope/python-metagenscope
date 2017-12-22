from __future__ import division

import os

import pytest

from metagenscope_cli.tools.kraken import kraken_data


@pytest.fixture
def kraken_file():
    filename = os.path.join(os.path.dirname(__file__), 'results/kraken.tsv')
    return open(filename)


def test_kraken_data(kraken_file):
    total_abundance = 7398030
    data = kraken_data(kraken_file, 0, 1)
    assert data[0]['taxon'] == 'd__Viruses'
    assert data[0]['abundance'] == pytest.approx(1733 / total_abundance)
    assert data[1]['taxon'] == 'd__Bacteria'
    assert data[1]['abundance'] == pytest.approx(7396285 / total_abundance)
    assert data[2]['taxon'] == 'd__Archaea'
    assert data[2]['abundance'] == pytest.approx(12 / total_abundance)
    assert data[3]['taxon'] == 'd__Bacteria|p__Proteobacteria'
    assert data[3]['abundance'] == pytest.approx(7285377 / total_abundance)
    assert data[4]['taxon'] == 'd__Archaea|p__Euryarchaeota|c__Methanomicrobia'
    assert data[4]['abundance'] == pytest.approx(2 / total_abundance)
    assert data[5]['taxon'] == 'd__Viruses|o__Caudovirales'
    assert data[5]['abundance'] == pytest.approx(1694 / total_abundance)
