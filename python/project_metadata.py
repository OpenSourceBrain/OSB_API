"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

project_ids = ['drosophila_projection_neuron', 'grancelllayer', 'muscle_model']

from osb import get_project, is_nml2_file

from osb.metadata import RDF, Description, add_simple_qualifier
from osb.resources import KNOWN_SPECIES, KNOWN_BRAIN_REGIONS



import time

info = "\n    This file has been automatically generated from data extracted from OSB project: %s\n" + \
       "    Generated on %s\n" + \
       "\n    Structure of this file subject to change without notice!!\n" + \
       "    Contact P Gleeson for more details\n        "

for project_id in project_ids:
    
    project = get_project(project_id)
    
    print("%s\tProject: %s (%s)\n" % ("-"*8, project.name, project.identifier))
    
    
    rdf = RDF(info%(project.identifier, time.strftime("%c")))
    desc = Description(project.identifier)
    rdf.descriptions.append(desc)
    
    # ID of the project on OSB
    add_simple_qualifier(desc, \
                         'bqmodel', \
                         'is', \
                         "http://opensourcebrain.org/projects/%s" % project.identifier, \
                         "Open Source Brain project identifier: %s" % project.identifier)
    
    # It's a computational neuroscience model
    add_simple_qualifier(desc, \
                        'bqbiol', \
                        'hasProperty', \
                        'http://identifiers.org/mamo/MAMO_0000026', \
                        "It's a computational neuroscience model")
                        
    # Species info
    species = project.species.lower()
    
    if species and KNOWN_SPECIES.has_key(species):
        add_simple_qualifier(desc, \
                             'bqbiol', \
                             'hasTaxon', \
                             'http://identifiers.org/taxonomy/%s'%KNOWN_SPECIES[species], \
                             "Open Source Brain species: %s; taxonomy id: %s" % (species, KNOWN_SPECIES[species]))
   
    # Brain region info
    brain_region = project.brain_region.lower()
    
    if brain_region and KNOWN_BRAIN_REGIONS.has_key(brain_region):
        add_simple_qualifier(desc, \
                             'bqbiol', \
                             'isPartOf', \
                             'http://identifiers.org/neurolex/%s'%KNOWN_BRAIN_REGIONS[brain_region], \
                             "Open Source Brain: %s; NeuroLex id: %s" % (brain_region, KNOWN_BRAIN_REGIONS[brain_region]))
                             
    github_repo = project.github_repo
            
    if github_repo is not None:

        files = github_repo.list_files_in_repo()
        for file in files:
            if is_nml2_file(file):
                desc = Description(file)
                desc.comment = "NeuroML 2 file: %s"%file
                #rdf.descriptions.append(desc)
                         

    print(rdf.to_xml())
    file = open('%s.xml'%project.identifier,'w')
    file.write(rdf.to_xml())
    file.close()