'''
API to OSB tests using restkit...
'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

projects = res.get('/projects.json', limit=1000)


jp = json.loads(projects.body_string())

from __init__ import get_custom_field,print_custom_field

for project in jp["projects"]:

    isProj = False
    hasMDB = False
    for cf in project["custom_fields"]:
        if cf['name'] == 'Category' and cf.has_key('value') \
                                    and cf['value']=='Project':
            isProj = True
        if cf['name'] == 'ModelDB reference' and cf.has_key('value') \
                                             and len(cf['value'])>0:
            hasMDB = True
    
    if isProj:
        print "\n--------   Project: %s\n" % project["name"]

        if hasMDB:
            print "\tOSB link:%shttp://opensourcebrain.org/projects/%s" % \
                                                (" "*22,project["identifier"])
            print_custom_field(project, 'ModelDB reference')
        else:
            print "\tNo ModelDB info for model"

        
