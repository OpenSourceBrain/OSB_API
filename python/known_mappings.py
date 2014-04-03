"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

# From http://www.ncbi.nlm.nih.gov/taxonomy
known_species = {}
known_species['rat'] = '10116'
known_species['mouse'] = '10090'
known_species['rodent'] = '9989'
known_species['drosophila'] = '7227'
known_species['c. elegans'] = '6239'
known_species['caenorhabditis elegans'] = '6239'


known_brain_regions = {}
known_brain_regions['cerebellum'] = 'birnlex_1489'
known_brain_regions['neocortex'] = 'birnlex_2547'


