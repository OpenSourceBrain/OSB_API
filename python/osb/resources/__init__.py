"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

# From http://www.ncbi.nlm.nih.gov/taxonomy
KNOWN_SPECIES = {}
KNOWN_SPECIES['rat'] = '10116'
KNOWN_SPECIES['mouse'] = '10090'
KNOWN_SPECIES['rodent'] = '9989'
KNOWN_SPECIES['drosophila'] = '7227'
KNOWN_SPECIES['c. elegans'] = '6239'
KNOWN_SPECIES['caenorhabditis elegans'] = '6239'


KNOWN_BRAIN_REGIONS = {}
KNOWN_BRAIN_REGIONS['cerebellum'] = 'birnlex_1489'
KNOWN_BRAIN_REGIONS['neocortex'] = 'birnlex_2547'


