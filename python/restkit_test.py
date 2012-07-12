'''
Preliminary tests using restkit...
'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')
r = res.get('/users/4.json')

import json

jr = json.loads(r.body_string())

print "User: "+str(jr["user"]["id"]) +" is "+jr["user"]["firstname"] +" "+jr["user"]["lastname"] 

p = res.get('/projects.json')


jp = json.loads(p.body_string())

for project in jp["projects"]:
    print "--------   Project: "+ project["name"] + "\n"
    print "    Last updated on:  "+ project["updated_on"]
    for cf in project["custom_fields"]:
        if cf['name'] == 'GitHub repository' and cf.has_key('value'):
            print "    GitHub repository: "+ cf['value']
    #print project
    print
