'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

p = res.get('/projects.json')

jp = json.loads(p.body_string())

passed = 1

import urllib

for project in jp["projects"]:
    print "--------   Project: "+ project["name"] +" ("+ project["identifier"] +")"+ "\n"
    #print "    Last updated on:  "+ project["updated_on"]
    status_found = 0
    github = 0
    category = ""
    spine_check = 0
    
    #print project["custom_fields"]
    
    for cf in project["custom_fields"]:
        if cf['name'] == 'GitHub repository' and cf.has_key('value'):
            #print "    GitHub repository: "+ cf['value']
            github = 1
        if cf['name'] == 'Status info' and cf.has_key('value'):
            status_found = 1
        if cf['name'] == 'Category' and cf.has_key('value'):
            category = cf['value']
        if cf['name'] == 'Spine classification' and cf.has_key('value'):
            spine_check = 1
            
            
        #  README & AUTHORS
        
        #  Sci Coord, developers, Sci Advisor

        # NML statuses

        # Simulator statuses

        # NML 1/2 native files?
        
    
           
    if category == "Project":
        if  status_found == 0:
            print "No status!"
            passed = 0
        if  spine_check == 0:
            print "Neither vertebrate nor invertebrate!"
            passed = 0

        if github == 1:
            f = urllib.urlopen("http://www.opensourcebrain.org/projects/"+project["identifier"]+"/repository/changes/README")
            if "The entry or revision was not found in the repository" in f.read():
                print "No README!"
                passed = 0
            w = urllib.urlopen("https://api.github.com/repos/OpenSourceBrain/"+project["identifier"])
            #print w.read()

    
print
if  passed == 0:
    print "    ****   FAILURE!   ****"
else:
    print "    ****   SUCCESS!   ****"
    
print
