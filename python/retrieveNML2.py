'''
Some quality assurance tests on OSB/GitHub repos

'''

import os
import sys

from lxml import etree
from urllib import urlopen

import osb

if __name__ == "__main__":
    
    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    count_nml2 = 0
    count_lems = 0
    count_nml2_invalid = 0
    count_lems_invalid = 0

    local = False

    versionFolder = "NeuroML2"
    nml_schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2beta.xsd")
    nml_suffix = ".nml"

    
    nml2 = True 

    if len(sys.argv) == 2 and sys.argv[1] == '-v1':
        print "Only looking for NeuroML v1 files"
        versionFolder = "NeuroML"
        nml_schema_file = urlopen("http://www.neuroml.org/NeuroMLValidator/NeuroMLFiles/Schemata/v1.8.1/Level3/NeuroML_Level3_v1.8.1.xsd")
        nml_suffix = ".xml"
        nml2 = False

    if len(sys.argv) == 2 and sys.argv[1]=='-local':
        local = True

    if local: print "Only checking local NeuroML files"


    xmlschema_doc = etree.parse(nml_schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    for project in osb.get_project_list(min_curation_level="None", limit=project_num):
        
        print "--------   Project: "+ project["name"] +" ("+ project["identifier"] +")"+ "\n"
        status_found = 0
        github_repo = None
        category = ""
        spine_check = 0
        endorsed = -1

        for cf in project["custom_fields"]:
            if cf['name'] == 'GitHub repository' and cf.has_key('value'):
                print "    GitHub repository: "+ cf['value']
                github_repo = cf['value']
            if cf['name'] == 'Endorsement' and cf.has_key('value'):
                endorsed = int(cf['value'])
                #print endorsed
                
		if github_repo.endswith(".git"):
			github_repo = github_repo[:-4]
            if cf['name'] == 'Status info' and cf.has_key('value') and len(cf['value']) > 0:
                status_found = 1
            if cf['name'] == 'Category' and cf.has_key('value'):
                category = cf['value']

        ignores = []
        ignores = ['blender-to-neuroml', \
        'olfactory-bulb-network-model-o-connor-angelo-and-jacob-2012']
        

        if category == "Project" and project["identifier"] not in ignores and endorsed == 1:

            if github_repo is not None and len(github_repo) > 0:

                if not os.path.exists(versionFolder):
                    os.makedirs(versionFolder)

                projFolder = versionFolder+"/"+project["identifier"]
                if not os.path.exists(projFolder):
                    os.makedirs(projFolder)

                if not local:
                    files = osb.list_files_in_repo(github_repo[19:])
                    #print("Checking files in: %s: %s"%(github_repo[19:], files))
                else:
                    files = os.listdir(projFolder)
                    print("Checking local files in: %s"%(projFolder))
                    
                
                for full_file_path in files:
                    
                    file_name = full_file_path.split('/')[-1]
                    local_file = projFolder+"/"+file_name

                    if file_name.endswith(nml_suffix):
                        #print "Checking NeuroML file: %s"%full_file_path
                        if not local:
                            url_file = "https://raw.github.com/%s/master/%s"%(github_repo[19:], full_file_path)
                            osb.copy_file_from_url(url_file, local_file)
                        else:
                            print "  Local file:  "+local_file,


                        if file_name.endswith(nml_suffix):
                            check = ' against schema only'
                            if not nml2 or os.getenv('JNML_HOME') is None:
                                doc = etree.parse(local_file)
                                valid = xmlschema.validate(doc)
                            else:
                                check = ' against jNeuroML'
                                ret = osb.check_jnml_validates_neuroml(local_file)
                                valid = not bool(ret)

                            if valid:
                                print "                 (Valid %s file%s)"%(versionFolder,check)
                                count_nml2+=1
                            else:
                                print "\n\n       It's NOT a valid %s file%s!\n"%(versionFolder,check)
                                count_nml2_invalid+=1
                                
                             
                for full_file_path in files:
                    file_name = full_file_path.split('/')[-1]
                    local_file = projFolder+"/"+file_name

                    if osb.is_lems_file(file_name):
                        print "Checking LEMS file: %s"%full_file_path
                        if not local:
                            url_file = "https://raw.github.com/%s/master/%s"%(github_repo[19:], full_file_path)
                            osb.copy_file_from_url(url_file, local_file)
                        else:
                            print "  Local file:  "+local_file,


                        if os.getenv('JNML_HOME') is not None:

                            ret = osb.check_jnml_loads_lems(local_file)
                            valid = not bool(ret)
                            if valid:
                                print "                 (Parsable LEMS file)"
                                count_lems+=1
                            else:
                                print "\n\n       It's NOT a parsable LEMS file!\n"
                                count_lems_invalid+=1
               
    print
    print "Found %i valid (%i invalid) NeuroML 2 files and %i parsable (%i not parsable) LEMS files"%(count_nml2, count_nml2_invalid,count_lems, count_lems_invalid)
    print
