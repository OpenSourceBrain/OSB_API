'''
Generate metadata for an OSB project
'''

project_ids = ['drosophila_projection_neuron', 'grancelllayer', 'muscle_model']

from __init__ import get_project, get_custom_field

from metadata import *
from known_mappings import *

def add_simple_qualifier(rdf, type, qualifier, resource, comment=None):
    bq = Qualifier(type,qualifier)
    bq.resources.append(resource)
    if comment: 
        bq.comment = comment
    rdf.qualifiers.append(bq)

for project_id in project_ids:
    
    project = get_project(project_id)
    project_name = project["name"]
    identifier = project["identifier"]
    
    print "%s\tProject: %s (%s)\n" % ("-"*8, project_name, identifier)
    
    
    rdf = RDF(identifier)
    
    # ID of the project on OSB
    add_simple_qualifier(rdf, \
                         'bqmodel', \
                         'is', \
                         "http://opensourcebrain.org/projects/%s" % identifier, \
                         "Open Source Brain project identifier: %s" % identifier)
    
    # It's a computational neuroscience model
    add_simple_qualifier(rdf, \
                        'bqbiol', \
                        'hasProperty', \
                        'http://identifiers.org/mamo/MAMO_0000026', \
                        "It's a computational neuroscience model")
                        
    # Species info
    species = get_custom_field(project, "Specie").lower()
    
    if species and known_species.has_key(species):
        add_simple_qualifier(rdf, \
                             'bqbiol', \
                             'hasTaxon', \
                             'http://identifiers.org/taxonomy/%s'%known_species[species], \
                             "Open Source Brain species: %s; taxonomy id: %s" % (species, known_species[species]))
   
    # Brain region info
    brain_region = get_custom_field(project, "Brain region").lower()
    
    if brain_region and known_brain_regions.has_key(brain_region):
        add_simple_qualifier(rdf, \
                             'bqbiol', \
                             'isPartOf', \
                             'http://identifiers.org/neurolex/%s'%known_brain_regions[brain_region], \
                             "Open Source Brain: %s; NeuroLex id: %s" % (brain_region, known_brain_regions[brain_region]))
                         

    print rdf.to_xml()
    file = open('%s.xml'%identifier,'w')
    file.write(rdf.to_xml())
    file.close()