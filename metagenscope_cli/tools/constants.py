"""MetaGenScope CLI constants.

N.B. tool types and file types are defined in the
metasub cap and stored in datasuper.
"""

# tool types
KRAKEN = 'kraken_taxonomy_profiling'
METAPHLAN2 = 'metaphlan2_taxonomy_profiling'
HMP_SITES = 'hmp_site_dists'
MICROBE_CENSUS = 'microbe_census'
SHORTBRED_AMRS = 'shortbred_amr_profiling'
RESISTOME_AMRS = 'resistome_amrs'
READ_CLASS_PROPS = 'read_classification_proportions'
READ_STATS = 'read_stats'
MICROBE_DIRECTORY = 'microbe_directory_annotate'
ALPHA_DIVERSITY = 'alpha_diversity_stats'
HUMANN2 = 'humann2_functional_profiling'
HUMANN2_NORMALIZED = 'humann2_normalize_genes'
METHYLS = 'align_to_methyltransferases'
VFDB = 'vfdb_quantify'


# other
TAXON_KEY = 'taxon'
ABUNDANCE_KEY = 'abundance'

AGS_KEY = 'average_genome_size'
TOTAL_BASES_KEY = 'total_bases'
GENOME_EQUIVALENTS_KEY = 'genome_equivalents'


# humann2
PATHWAY_KEY = 'pathway'
ABUNDANCE_KEY = 'abundance'
COVERAGE_KEY = 'coverage'
GENE_KEY = 'gene_family'

# Gene Quantification
GENE_ID = 'gene_name'
RPK_KEY = 'RPK'
RPKM_KEY = 'RPKM'
RPKMG_KEY = 'RPKG'
