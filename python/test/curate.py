'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

p = res.get('/projects.json')

jp = json.loads(p.body_string())

passed = 1



for project in jp["projects"]:
    print "--------   Project: "+ project["name"] + "\n"
    #print "    Last updated on:  "+ project["updated_on"]
    status_found = 0
    github = 0
    category = ""
    
    for cf in project["custom_fields"]:
        if cf['name'] == 'GitHub repository' and cf.has_key('value'):
            #print "    GitHub repository: "+ cf['value']
            github = 1
        if cf['name'] == 'Status info' and cf.has_key('value'):
            status_found = 1
        if cf['name'] == 'Category' and cf.has_key('value'):
            category = cf['value']
           
    if  status_found == 0 and category == "Project":
        print "No status!"
       
        passed = 0

    
print
if  passed == 0:
    print "    ****   FAILURE!   ****"
else:
    print "    ****   SUCCESS!   ****"
    
print
