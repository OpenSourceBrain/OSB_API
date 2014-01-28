'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
import os
import sys

import json

from lxml import etree
from urllib import urlopen
import subprocess

from __init__ import check_file_in_repository,list_files_in_repo_dir
from __init__ import copy_file_from_url,check_jnml_validates_NeuroML
from __init__ import check_jnml_loads_lems
    
if __name__ == "__main__":

    count_nml2 = 0
    count_lems = 0
    count_nml2_invalid = 0
    count_lems_invalid = 0

    res = Resource('http://www.opensourcebrain.org')

    p = res.get('/projects.json', limit=3000)

    jp = json.loads(p.body_string())

    local = False


    versionFolder = "NeuroML2"
    url = "https://raw.github.com/NeuroML/NeuroML2/master/"
    url += "Schemas/NeuroML2/NeuroML_v2beta.xsd"
    nml_schema_file = urlopen(url)
    nml_suffix = ".nml"

    lems_suffix = ".xml"
    lems_prefix1 = "Run_"
    lems_prefix2 = "LEMS_"
    
    nml2 = True 

    if len(sys.argv) == 2 and sys.argv[1] == '-v1':
        print "Only looking for NeuroML v1 files"
        versionFolder = "NeuroML"
        url = "http://www.neuroml.org/NeuroMLValidator/NeuroMLFiles/"
        url += "Schemata/v1.8.1/Level3/NeuroML_Level3_v1.8.1.xsd"
        nml_schema_file = urlopen(url)
        nml_suffix = ".xml"
        nml2 = False

    if len(sys.argv) == 2 and sys.argv[1]=='-local':
        local = True

    if local: print "Only checking local NeuroML files"


    xmlschema_doc = etree.parse(nml_schema_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    for project in jp["projects"]:
        print "-"*8 + "   Project: %s (%s)\n" % \
                (project["name"],project["identifier"])
        status_found = 0
        github_repo = None
        category = ""
        spine_check = 0

        for cf in project["custom_fields"]:
            if cf['name'] == 'GitHub repository' and cf.has_key('value'):
                #print "    GitHub repository: "+ cf['value']
                github_repo = cf['value']
		if github_repo.endswith(".git"):
			github_repo = github_repo[:-4]
            if cf['name'] == 'Status info' and cf.has_key('value') \
                                           and len(cf['value']) > 0:
                status_found = 1
            if cf['name'] == 'Category' and cf.has_key('value'):
                category = cf['value']



        if category == "Project":

            if github_repo is not None and len(github_repo) > 0:

                nmlFolder = False
                genNmlFolder = False
                identifier = project["identifier"]

                if check_file_in_repository(identifier, versionFolder):
                    print "Found %s!"%versionFolder
                    nmlFolder = True
                nC_versionFolder = "neuroConstruct/generated"+versionFolder
                if check_file_in_repository(identifier, nC_versionFolder):
                    print "Found neuroConstruct/generated%s!"%versionFolder
                    genNmlFolder = True


                if nmlFolder or genNmlFolder:
                    if not os.path.exists(versionFolder):
                        os.makedirs(versionFolder)

                    projFolder = versionFolder+"/"+project["identifier"]
                    if not os.path.exists(projFolder):
                        os.makedirs(projFolder)

                    remoteFolder = nCversionFolder if genNmlFolder else versionFolder
                    if not local:
                        files = list_files_in_repo_dir(github_repo[19:], remoteFolder)
                    else:
                        files = os.listdir(projFolder)

                    #print files

                    for file in files:

                        local_file = projFolder+"/"+file

                        if not local:
                            url_file = "https://raw.github.com/%s/master/%s/%s" % \
                                        (github_repo[19:], remoteFolder, file)
                            copy_file_from_url(url_file, local_file)
                        else:
                            print "    "+local_file,


                        if file.endswith(nml_suffix):
                            check = ' against schema only'
                            if not nml2 or os.getenv('JNML_HOME') is None:
                                doc = etree.parse(local_file)
                                valid = xmlschema.validate(doc)
                            else:
                                check = ' against jNeuroML'
                                ret = check_jnml_validates_NeuroML(local_file)
                                valid = not bool(ret)

                            if valid:
                                print "%s(Valid %s file%s)"%(" "*17,versionFolder,check)
                                count_nml2+=1
                            else:
                                print "\n\n%sIt's NOT a valid %s file%s!\n"%(" "*7,versionFolder,check)
                                count_nml2_invalid+=1

                        elif file.endswith(lems_suffix) and (file.startswith(lems_prefix1) \
                                                        or file.startswith(lems_prefix2)):
                            
                            if os.getenv('JNML_HOME') is not None:

                                ret = check_jnml_loads_lems(local_file)
                                valid = not bool(ret)
                                if valid:
                                    print "%s(Parsable LEMS file)" % " "*17
                                    count_lems+=1
                                else:
                                    print "\n\n%sIt's NOT a parsable LEMS file!\n" % " "*7
                                    count_lems_invalid+=1
                            else:
                                print "%s---- LEMS ----" % " "*17
                        else:
                            print "%s-----" % " "*17
    print
    result = "Found %i valid (%i invalid) NeuroML 2 files" % (count_nml2, count_nml2_invalid)
    result += " and %i parsable (%i not parsable) LEMS files" % (count_lems, count_lems_invalid)
    print result
    print
