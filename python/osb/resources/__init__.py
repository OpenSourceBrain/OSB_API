"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

OSB_PROJECT_URL_TEMPLATE = "http://opensourcebrain.org/projects/%s"

PUBMED_URL_TEMPLATE = "http://identifiers.org/pubmed/%s"


# From http://www.ncbi.nlm.nih.gov/taxonomy
NCBI_TAXONOMY_URL_TEMPLATE = 'http://identifiers.org/taxonomy/%s'
KNOWN_SPECIES = {}
KNOWN_SPECIES['rat'] = '10116'
KNOWN_SPECIES['cat'] = '9685'
KNOWN_SPECIES['mouse'] = '10090'
KNOWN_SPECIES['rodent'] = '9989'
KNOWN_SPECIES['drosophila'] = '7227'
KNOWN_SPECIES['c. elegans'] = '6239'
KNOWN_SPECIES['caenorhabditis elegans'] = '6239'
KNOWN_SPECIES['human'] = '1758'
# as used by Channelpedia
KNOWN_SPECIES['xenopus'] = '262014'
KNOWN_SPECIES['chinese hamster'] = '10029'
KNOWN_SPECIES['crab'] = '6752'  # Brachyura, short-tailed crabs
KNOWN_SPECIES['squid'] = '551290' # Teuthida, cephalopods


# This is not working for all neurolex ids, e.g. http://identifiers.org/neurolex/nifext_128 
#NEUROLEX_URL_TEMPLATE = 'http://identifiers.org/neurolex/%s'
NEUROLEX_URL_TEMPLATE = 'http://neurolex.org/wiki/%s'

# Use NeuroLex IDs
KNOWN_BRAIN_REGIONS = {}
KNOWN_BRAIN_REGIONS['cerebellum'] = 'birnlex_1489'
KNOWN_BRAIN_REGIONS['neocortex'] = 'birnlex_2547'


# Use NeuroLex IDs
KNOWN_CELL_TYPES = {}
KNOWN_CELL_TYPES['cerebellum:granule cell'] = 'nifext_128'
KNOWN_CELL_TYPES['cerebellum:golgi cell'] = 'sao1415726815'
KNOWN_CELL_TYPES['cerebellum:purkinje cell'] = 'sao471801888'
# as used by Channelpedia
KNOWN_CELL_TYPES['cerebellar purkinje'] = 'sao471801888'
KNOWN_CELL_TYPES['dorsal root ganglion'] = 'birnlex_2596'
KNOWN_CELL_TYPES['neocortical l5pc'] = 'nifext_50'        # Neocortex pyramidal cell layer 5-6
KNOWN_CELL_TYPES['l5pc'] = 'nifext_50'                    # Neocortex pyramidal cell layer 5-6


MAMO_URL_TEMPLATE = 'http://identifiers.org/mamo/%s'

KNOWN_MAMO_CLASSES = {}
KNOWN_MAMO_CLASSES['computational neuroscience model'] = 'MAMO_0000026'


GO_URL_TEMPLATE = 'http://identifiers.org/go/%s'

KNOWN_GO_TERMS = {}
KNOWN_GO_TERMS['ion channel complex'] = 'GO:0034702'
KNOWN_GO_TERMS['calcium channel complex'] = 'GO:0034704'
KNOWN_GO_TERMS['potassium channel complex'] = 'GO:0034705'
KNOWN_GO_TERMS['sodium channel complex'] = 'GO:0034706'


CNO_URL_TEMPLATE = 'http://purl.org/incf/ontology/Computational_Neurosciences/cno_alpha.owl#%s'

KNOWN_CNO_TERMS = {}
KNOWN_CNO_TERMS['ionic current model'] = 'cno_0000047'
KNOWN_CNO_TERMS['biophysical spiking model'] = 'cno_0000017'