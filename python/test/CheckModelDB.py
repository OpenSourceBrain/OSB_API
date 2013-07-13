'''
API to OSB tests using restkit...
'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

projects = res.get('/projects.json', limit=1000)


jp = json.loads(projects.body_string())


def printCustomField(project, cfName):
    for cf in project["custom_fields"]:
        if cf['name'] == cfName and cf.has_key('value'):  
            if cfName == 'ModelDB reference':
                print "    ModelDB link:                  http://senselab.med.yale.edu/ModelDB/ShowModel.asp?model=%s"%cf['value']
            else:
                print "     "+cfName+":             "+ cf['value']

for project in jp["projects"]:

    isProj = False
    hasMDB = False
    for cf in project["custom_fields"]:
        if cf['name'] == 'Category' and cf.has_key('value') and cf['value']=='Project':
            isProj = True
        if cf['name'] == 'ModelDB reference' and cf.has_key('value') and len(cf['value'])>0:
            hasMDB = True
    
    if isProj:
        print "\n--------   Project: "+ project["name"] + "\n"

        if hasMDB:
            print "    OSB link:                      http://opensourcebrain.org/projects/"+project["identifier"]
            printCustomField(project, 'ModelDB reference')
        else:
            print "    No ModelDB info for model"

        
