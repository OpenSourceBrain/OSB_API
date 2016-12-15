'''
Some quality assurance tests on OSB/GitHub repos

'''

import os
import sys

from lxml import etree
try:
    from urllib2 import urlopen  # Python 2
except:
    from urllib.request import urlopen # Python 3

import osb

if __name__ == "__main__":
    
    project_num = 1000
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        project_num = int(sys.argv[1])

    count_nml2 = 0
    count_lems = 0
    count_projs = 0
    count_nml2_invalid = 0
    count_lems_invalid = 0

    local = False

    versionFolder = "NeuroML2"
    nml_schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2beta.xsd")
    nml_suffix = ".nml"

    
    nml2 = True 

    if len(sys.argv) == 2 and sys.argv[1] == '-v1':
        print("Only looking for NeuroML v1 files")
        versionFolder = "NeuroML"
        nml_schema_file = urlopen("http://www.neuroml.org/NeuroMLValidator/NeuroMLFiles/Schemata/v1.8.1/Level3/NeuroML_Level3_v1.8.1.xsd")
        nml_suffix = ".xml"
        nml2 = False

    if len(sys.argv) == 2 and sys.argv[1]=='-local':
        local = True

    if local: print("Only checking local NeuroML files")


    xmlschema_doc = etree.parse(nml_schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    for project in osb.get_projects(min_curation_level="None", limit=project_num):
        
        print("\n--------   Project: "+ project.name +" ("+ project.identifier +")"+ "\n")

        ignores = ['blender-to-neuroml', 
                   'olfactory-bulb-network-model-o-connor-angelo-and-jacob-2012',
                   'neurosciences-repository']
        
        if project_num<30:
                   ignores += ['miglioreetal14_olfactorybulb3d', # Lots of NML2... 
                   'alleninstituteneuroml', # Lots of NML2... 
                   'blue-brain-project-showcase'] # Lots of NML2... 

        if not ( project.is_standard_project() or project.is_showcase()):
            print("  (Ignoring project as its category is: %s)  "%project.category)
        
        elif project.identifier in ignores:
            print("  (Ignoring project)  ")
        
        elif project.endorsement != 1:
            print("  (Ignoring project as its endorsement is: %s)  "%project.endorsement)
            
        else:
            github_repo = project.github_repo
            if github_repo is None:
                print("  (No GitHub repository)  ")
            else:
                
                some_valid = False

                if not os.path.exists(versionFolder):
                    os.makedirs(versionFolder)

                projFolder = versionFolder+"/"+project.identifier
                if not os.path.exists(projFolder):
                    os.makedirs(projFolder)

                if not local:
                    files = github_repo.list_files_in_repo()
                    print("  (Found %i files in repo)"%(len(files)))
                else:
                    files = os.listdir(projFolder)
                    print("Checking local files in: %s"%(projFolder))
                    
                
                for full_file_path in files:
                    
                    file_name = full_file_path.split('/')[-1]
                    local_file = projFolder+"/"+file_name

                    if file_name.endswith(nml_suffix):
                        print "  ...Getting NeuroML file: %s"%full_file_path
                        if not local:
                            github_repo.copy_file_from_repository(full_file_path, local_file)
                        else:
                            print("  Local file:  "+local_file,)


                        if file_name.endswith(nml_suffix):
                            check = ' against schema only'
                            if not nml2 or os.getenv('JNML_HOME') is None:
                                doc = etree.parse(local_file)
                                valid = xmlschema.validate(doc)
                            else:
                                check = ' against jNeuroML'
                                ret = osb.utils.check_jnml_validates_neuroml(local_file)
                                valid = not bool(ret)

                            if valid:
                                print("                 (Valid %s file%s)"%(versionFolder,check))
                                count_nml2+=1
                                some_valid = True
                            else:
                                print("\n\n       It's NOT a valid %s file%s!\n"%(versionFolder,check))
                                count_nml2_invalid+=1
                                
                             
                for full_file_path in files:
                    file_name = full_file_path.split('/')[-1]
                    local_file = projFolder+"/"+file_name

                    if osb.utils.is_lems_file(file_name):
                        print("Checking LEMS file: %s"%full_file_path)
                        if not local:
                            github_repo.copy_file_from_repository(full_file_path, local_file)
                        else:
                            print("  Local file:  "+local_file,)


                        if os.getenv('JNML_HOME') is not None:

                            ret = osb.utils.check_jnml_loads_lems(local_file)
                            valid = not bool(ret)
                            if valid:
                                print("                 (Parsable LEMS file)")
                                count_lems+=1
                                some_valid = True
                            else:
                                print("\n\n       It's NOT a parsable LEMS file!\n")
                                count_lems_invalid+=1
                                
                if some_valid:
                    count_projs +=1
                                
            print("\nSo far %i valid (%i invalid) NeuroML 2 files and %i parsable (%i not parsable) LEMS files.\n%i projects with some valid NeuroML2/LEMS\n"%(count_nml2, count_nml2_invalid,count_lems, count_lems_invalid, count_projs))
         
    print("\nFound %i valid (%i invalid) NeuroML 2 files and %i parsable (%i not parsable) LEMS files.\n%i projects with some valid NeuroML2/LEMS\n"%(count_nml2, count_nml2_invalid,count_lems, count_lems_invalid, count_projs))
    
