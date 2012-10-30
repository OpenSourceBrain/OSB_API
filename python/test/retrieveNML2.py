'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

p = res.get('/projects.json', limit=1000)

jp = json.loads(p.body_string())

import urllib
import os

from lxml import etree
from urllib import urlopen

nml2_schema_file = urlopen("http://neuroml.svn.sourceforge.net/viewvc/neuroml/NeuroML2/Schemas/NeuroML2/NeuroML_v2alpha.xsd")

xmlschema_doc = etree.parse(nml2_schema_file)
xmlschema = etree.XMLSchema(xmlschema_doc)

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

            nml2Folder = False
            genNml2Folder = False

            if checkFileInRepository(project["identifier"], "NeuroML2"):
                print "Found NeuroML2!"
                nml2Folder = True
            if checkFileInRepository(project["identifier"], "neuroConstruct/generatedNeuroML2"):
                print "Found neuroConstruct/generatedNeuroML2!"
                genNml2Folder = True


            if nml2Folder or genNml2Folder:
                if not os.path.exists("NeuroML2"):
                    os.makedirs("NeuroML2")

                projFolder = "NeuroML2/"+project["identifier"]
                if not os.path.exists(projFolder):
                    os.makedirs(projFolder)
                
                remoteFolder = "neuroConstruct/generatedNeuroML2" if genNml2Folder else "NeuroML2"
                files = listFilesInRepoDir(github_repo[19:], remoteFolder)

                for file in files:
                    url_file = "https://raw.github.com/%s/master/%s/%s"%(github_repo[19:], remoteFolder, file)
                    local_file = projFolder+"/"+file
                    copyFileFromUrl(url_file, local_file)

                    if file.endswith(".nml"):
                        doc = etree.parse(local_file)
                        valid = xmlschema.validate(doc)
                        if not valid:
                            print "  It's NOT a valid NeuroML 2 file!"

    
print
