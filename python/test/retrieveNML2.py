'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
import urllib
import os
import sys

import json

from lxml import etree
from urllib import urlopen
import subprocess


def check_file_in_repository(projectId, filename):
    f = urllib.urlopen("http://www.opensourcebrain.org/projects/%s/repository/changes/%s" % (projectId, filename))
    if "The entry or revision was not found in the repository" in f.read():
        return False
    else:
        return True
    
def list_files_in_repo_dir(gh_repo, dirname):
    rest_url = "https://api.github.com/repos/%s/contents/%s"%(gh_repo, dirname)
    w = urllib.urlopen(rest_url)
    json_files = json.loads(w.read())
    files = []
    for entry in json_files:
        #print entry
        files.append(entry["name"])
    return files

def copy_file_from_url(url_file, target_file):
    f = urllib.urlopen(url_file)
    t = open(target_file, 'w')
    t.write(f.read())
    print "Created: "+target_file,

def check_jnml_validates_NeuroML(document):
    p = subprocess.Popen(["jnml -validate "+ document], shell=True, stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode

def check_jnml_loads_lems(document):
    p = subprocess.Popen(["jnml "+ document+ " -norun"], shell=True, stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode

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
    nml_schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2beta.xsd")
    nml_suffix = ".nml"

    lems_suffix = ".xml"
    lems_prefix1 = "Run_"
    lems_prefix2 = "LEMS_"
    
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

    for project in jp["projects"]:
        print "--------   Project: "+ project["name"] +" ("+ project["identifier"] +")"+ "\n"
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
            if cf['name'] == 'Status info' and cf.has_key('value') and len(cf['value']) > 0:
                status_found = 1
            if cf['name'] == 'Category' and cf.has_key('value'):
                category = cf['value']



        if category == "Project":

            if github_repo is not None and len(github_repo) > 0:

                nmlFolder = False
                genNmlFolder = False

                if check_file_in_repository(project["identifier"], versionFolder):
                    print "Found %s!"%versionFolder
                    nmlFolder = True
                if check_file_in_repository(project["identifier"], "neuroConstruct/generated"+versionFolder):
                    print "Found neuroConstruct/generated%s!"%versionFolder
                    genNmlFolder = True


                if nmlFolder or genNmlFolder:
                    if not os.path.exists(versionFolder):
                        os.makedirs(versionFolder)

                    projFolder = versionFolder+"/"+project["identifier"]
                    if not os.path.exists(projFolder):
                        os.makedirs(projFolder)

                    remoteFolder = "neuroConstruct/generated"+versionFolder if genNmlFolder else versionFolder
                    if not local:
                        files = list_files_in_repo_dir(github_repo[19:], remoteFolder)
                    else:
                        files = os.listdir(projFolder)

                    #print files

                    for file in files:

                        local_file = projFolder+"/"+file

                        if not local:
                            url_file = "https://raw.github.com/%s/master/%s/%s"%(github_repo[19:], remoteFolder, file)
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
                                print "                 (Valid %s file%s)"%(versionFolder,check)
                                count_nml2+=1
                            else:
                                print "\n\n       It's NOT a valid %s file%s!\n"%(versionFolder,check)
                                count_nml2_invalid+=1

                        elif file.endswith(lems_suffix) and (file.startswith(lems_prefix1) or file.startswith(lems_prefix2)):
                            
                            if os.getenv('JNML_HOME') is not None:

                                ret = check_jnml_loads_lems(local_file)
                                valid = not bool(ret)
                                if valid:
                                    print "                 (Parsable LEMS file)"
                                    count_lems+=1
                                else:
                                    print "\n\n       It's NOT a parsable LEMS file!\n"
                                    count_lems_invalid+=1
                            else:
                                print     "                 ---- LEMS ----"
                        else:
                            print     "                 -----"
    print
    print "Found %i valid (%i invalid) NeuroML 2 files and %i parsable (%i not parsable) LEMS files"%(count_nml2, count_nml2_invalid,count_lems, count_lems_invalid)
    print
