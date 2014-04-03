"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

project_ids = ['drosophila_projection_neuron', 'grancelllayer', 'muscle_model']

import osb

from metadata import *
from known_mappings import *

import time

info = "\n    This file has been automatically generated from data extracted from OSB project: %s\n" + \
       "    Generated on %s\n" + \
       "\n    Structure of this file subject to change without notice!!\n" + \
       "    Contact P Gleeson for more details\n        "


def add_simple_qualifier(rdf, type, qualifier, resource, comment=None):
    bq = Qualifier(type,qualifier)
    bq.resources.append(resource)
    if comment: 
        bq.comment = comment
    rdf.qualifiers.append(bq)

for project_id in project_ids:
    
    project = osb.get_project(project_id)
    
    print("%s\tProject: %s (%s)\n" % ("-"*8, project.name, project.identifier))
    
    
    rdf = RDF(project.identifier)
    rdf.comment = info%(project.identifier, time.strftime("%c"))
    
    # ID of the project on OSB
    add_simple_qualifier(rdf, \
                         'bqmodel', \
                         'is', \
                         "http://opensourcebrain.org/projects/%s" % project.identifier, \
                         "Open Source Brain project identifier: %s" % project.identifier)
    
    # It's a computational neuroscience model
    add_simple_qualifier(rdf, \
                        'bqbiol', \
                        'hasProperty', \
                        'http://identifiers.org/mamo/MAMO_0000026', \
                        "It's a computational neuroscience model")
                        
    # Species info
    species = project.species.lower()
    
    if species and known_species.has_key(species):
        add_simple_qualifier(rdf, \
                             'bqbiol', \
                             'hasTaxon', \
                             'http://identifiers.org/taxonomy/%s'%known_species[species], \
                             "Open Source Brain species: %s; taxonomy id: %s" % (species, known_species[species]))
   
    # Brain region info
    brain_region = project.brain_region.lower()
    
    if brain_region and known_brain_regions.has_key(brain_region):
        add_simple_qualifier(rdf, \
                             'bqbiol', \
                             'isPartOf', \
                             'http://identifiers.org/neurolex/%s'%known_brain_regions[brain_region], \
                             "Open Source Brain: %s; NeuroLex id: %s" % (brain_region, known_brain_regions[brain_region]))
                         

    print(rdf.to_xml())
    file = open('%s.xml'%project.identifier,'w')
    file.write(rdf.to_xml())
    file.close()