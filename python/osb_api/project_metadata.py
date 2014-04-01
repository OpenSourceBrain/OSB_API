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
    
    add_simple_qualifier(rdf, \
                         'bqmodel', \
                         'is', \
                         "http://opensourcebrain.org/projects/%s" % identifier, \
                         "Open Source Brain project identifier: %s" % identifier)
    
    species = get_custom_field(project, "Specie").lower()
    #print species
    if species and known_species.has_key(species):
        add_simple_qualifier(rdf, \
                             'bqbiol', \
                             'hasTaxon', \
                             'http://identifiers.org/taxonomy/%s'%known_species[species], \
                             "Open Source Brain species: %s; taxonomy id: %s" % (species, known_species[species]))
                         

    print rdf.to_xml()
    file = open('%s.xml'%identifier,'w')
    file.write(rdf.to_xml())
    file.close()