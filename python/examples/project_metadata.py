"""
    Work in progress towards extracting structured metadata from OSB projects
    
    Contact p.gleeson if you are interested in using this. Subject to change without notice!!
    
"""

project_ids = ['drosophila_projection_neuron', 'grancelllayer', 'muscle_model', 'granulecell']
#project_ids = ['grancelllayer']

from osb.Project import Project
from osb.utils import is_nml2_file, get_page

from osb.metadata import RDF, Description, add_simple_qualifier, parse_for_metadata
import osb.resources as osbres

from neuroml.nml.nml import parseString

import time

import sys

info = "\n    This file has been automatically generated from data extracted from OSB project: %s\n" + \
       "    Generated on %s\n" + \
       "\n    Structure of this file subject to change without notice!!\n" + \
       "    Contact P Gleeson for more details\n        "
       
unknowns = ""


if __name__ == "__main__":
    
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        project_ids = project_ids[0:int(sys.argv[1])]

    for project_id in project_ids:

        project = Project.get(project_id)

        print("%s\tProject: %s (%s)\n" % ("-"*8, project.name, project.identifier))


        rdf = RDF(info%(project.identifier, time.strftime("%c")))
        desc = Description(project.identifier)
        rdf.descriptions.append(desc)

        # ID of the project on OSB
        add_simple_qualifier(desc, \
                             'bqmodel', \
                             'is', \
                             osbres.OSB_PROJECT_URL_TEMPLATE % project.identifier, \
                             "Open Source Brain project identifier: %s" % project.identifier)


        # Species info
        species = project.species.lower()

        if species:
            if osbres.KNOWN_SPECIES.has_key(species):
                add_simple_qualifier(desc, \
                                     'bqbiol', \
                                     'hasTaxon', \
                                     osbres.NCBI_TAXONOMY_URL_TEMPLATE % osbres.KNOWN_SPECIES[species], \
                                     "OSB species: %s; taxonomy id: %s" % (species, osbres.KNOWN_SPECIES[species]))
            else:
                unknowns += "species: %s\n"%species

        # Brain region info
        brain_region = project.brain_region.lower()

        if brain_region:
            if osbres.KNOWN_BRAIN_REGIONS.has_key(brain_region):
                add_simple_qualifier(desc, \
                                     'bqbiol', \
                                     'isPartOf', \
                                     osbres.NEUROLEX_URL_TEMPLATE % osbres.KNOWN_BRAIN_REGIONS[brain_region], \
                                     "OSB brain region: %s; NeuroLex id: %s" % (brain_region, osbres.KNOWN_BRAIN_REGIONS[brain_region]))
            else:
                unknowns += "brain_region: %s\n"%brain_region

        # Cell type info
        cell_type = "%s:%s"%(brain_region, project.cell_type.lower())

        if cell_type:
            if osbres.KNOWN_CELL_TYPES.has_key(cell_type):
                add_simple_qualifier(desc, \
                                     'bqbiol', \
                                     'isPartOf', \
                                     osbres.NEUROLEX_URL_TEMPLATE % osbres.KNOWN_CELL_TYPES[cell_type], \
                                     "OSB cell type: %s; NeuroLex id: %s" % (cell_type, osbres.KNOWN_CELL_TYPES[cell_type]))
            else:
                unknowns += "cell_type: %s\n"%cell_type

        github_repo = project.github_repo

        if github_repo is not None:

            files = github_repo.list_files_in_repo()
            for file in files:
                if is_nml2_file(file):
                    desc = Description(file)
                    raw_url = github_repo.link_to_raw_file_in_repo(file)
                    comment = "NeuroML 2 file: %s (at %s)"%(file,raw_url)
                    rdf.descriptions.append(desc)

                    # It's a computational neuroscience model
                    add_simple_qualifier(desc, \
                                        'bqmodel', \
                                        'is', \
                                        raw_url, \
                                        "")


                    contents = get_page(raw_url)

                    print("  Building NeuroML doc from: "+raw_url)
                    cno_type = None
                    doc = parseString(contents)
                    if doc.notes:
                        comment += "\n%s"%doc.notes

                    for ion_channel in doc.ion_channel:
                        cno_type = 'ionic current model'
                        if ion_channel.notes:
                            comment += "\n  Ion Channel: %s; %s"%(ion_channel.id, ion_channel.notes)

                        channel_type = 'ion channel complex'
                        if ion_channel.species:
                            if ion_channel.species == "ca":
                                channel_type = 'calcium channel complex'
                            elif ion_channel.species == "na":
                                channel_type = 'sodium channel complex'
                            elif ion_channel.species == "k":
                                channel_type = 'potassium channel complex'

                        add_simple_qualifier(desc, \
                                        'bqbiol', \
                                        'is', \
                                        osbres.GO_URL_TEMPLATE % osbres.KNOWN_GO_TERMS[channel_type], \
                                        "It is a model of the GO entity: %s (species through ion channel: %s)" % (channel_type, ion_channel.species))

                        metadata = parse_for_metadata(contents)
                        if metadata.has_key(ion_channel.id):
                            desc.free_text += "        <!-- Metadata extracted from NeuroML file -->\n"+metadata[ion_channel.id]

                    for cell in doc.cells:
                        cno_type = 'biophysical spiking model'
                        if cell.notes:
                            comment += "\n  Cell: %s; %s"%(cell.id, cell.notes)
                        if cell.neuro_lex_id:
                            url = osbres.NEUROLEX_URL_TEMPLATE % cell.neuro_lex_id
                            add_simple_qualifier(desc, \
                                        'bqbiol', \
                                        'is', \
                                        url, \
                                        "It is a model of the NeuroLex entity: %s"%cell.neuro_lex_id)


                    if cno_type:
                        add_simple_qualifier(desc, \
                                            'bqbiol', \
                                            'hasProperty', \
                                            osbres.CNO_URL_TEMPLATE % osbres.KNOWN_CNO_TERMS[cno_type], \
                                            "It is of type: %s (CNO ID: %s)"%(cno_type, osbres.KNOWN_CNO_TERMS[cno_type]))

                    desc.comment = comment

                    print("--------------\n%s\n---------"%comment)



        print(rdf.to_xml())
        file = open('%s.xml'%project.identifier,'w')
        file.write(rdf.to_xml())
        file.close()


    unknowns_file = open('unknowns','w')
    unknowns_file.write(unknowns)
    unknowns_file.close()
