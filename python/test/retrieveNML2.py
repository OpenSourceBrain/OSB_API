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


def checkFileInRepository(projectId, filename):
    f = urllib.urlopen("http://www.opensourcebrain.org/projects/%s/repository/changes/%s" % (projectId, filename))
    if "The entry or revision was not found in the repository" in f.read():
        return False
    else:
        return True
    
def listFilesInRepoDir(gh_repo, dirname):
    rest_url = "https://api.github.com/repos/%s/contents/%s"%(gh_repo, dirname)
    w = urllib.urlopen(rest_url)
    json_files = json.loads(w.read())
    files = []
    for entry in json_files:
        files.append(entry["name"])
    return files

def copyFileFromUrl(url_file, target_file):
    f = urllib.urlopen(url_file)
    t = open(target_file, 'w')
    t.write(f.read())
    print "Created: "+target_file
    

if __name__ == "__main__":

    res = Resource('http://www.opensourcebrain.org')

    p = res.get('/projects.json', limit=1000)

    jp = json.loads(p.body_string())


    versionFolder = "NeuroML2"
    nml_schema_file = urlopen("https://raw.github.com/NeuroML/NeuroML2/master/Schemas/NeuroML2/NeuroML_v2beta.xsd")
    suffix = ".nml"

    if len(sys.argv) == 2 and sys.argv[1] == '-v1':
        print "Only looking for NeuroML v1 files"
        versionFolder = "NeuroML"
        nml_schema_file = urlopen("http://neuroml.svn.sourceforge.net/viewvc/neuroml/trunk/web/NeuroMLFiles/Schemata/v1.8.1/Level3/NeuroML_Level3_v1.8.1.xsd")
        suffix = ".xml"



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
            if cf['name'] == 'Status info' and cf.has_key('value') and len(cf['value']) > 0:
                status_found = 1
            if cf['name'] == 'Category' and cf.has_key('value'):
                category = cf['value']



        if category == "Project":

            if github_repo is not None:

                nmlFolder = False
                genNmlFolder = False

                if checkFileInRepository(project["identifier"], versionFolder):
                    print "Found %s!"%versionFolder
                    nmlFolder = True
                if checkFileInRepository(project["identifier"], "neuroConstruct/generated"+versionFolder):
                    print "Found neuroConstruct/generated%s!"%versionFolder
                    genNmlFolder = True


                if nmlFolder or genNmlFolder:
                    if not os.path.exists(versionFolder):
                        os.makedirs(versionFolder)

                    projFolder = versionFolder+"/"+project["identifier"]
                    if not os.path.exists(projFolder):
                        os.makedirs(projFolder)

                    remoteFolder = "neuroConstruct/generated"+versionFolder if genNmlFolder else versionFolder
                    files = listFilesInRepoDir(github_repo[19:], remoteFolder)

                    for file in files:
                        url_file = "https://raw.github.com/%s/master/%s/%s"%(github_repo[19:], remoteFolder, file)
                        local_file = projFolder+"/"+file
                        copyFileFromUrl(url_file, local_file)

                        if file.endswith(suffix):
                            doc = etree.parse(local_file)
                            valid = xmlschema.validate(doc)
                            if valid:
                                print "  It is a valid %s file"%versionFolder
                            else:
                                print "  It's NOT a valid %s file!"%versionFolder

    
    print
