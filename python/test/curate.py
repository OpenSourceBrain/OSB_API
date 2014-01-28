'''
Some quality assurance tests on OSB/GitHub repos

'''

from restkit import Resource
res = Resource('http://www.opensourcebrain.org')

import json

p = res.get('/projects.json', limit=1000)

jp = json.loads(p.body_string())

passed = 1

import urllib

from __init__ import check_file_in_repository, known_external_repo

for project in jp["projects"]:
    print "%sProject: %s (%s)\n" % ("-"*8,project["name"],project["identifier"])
    #print "    Last updated on:  "+ project["updated_on"]
    status_found = 0
    github_repo = None
    category = ""
    spine_check = 0
    
    #print project["custom_fields"]
    
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

        #print json.dumps(project, sort_keys=True, indent=4)

        if github_repo is not None and len(github_repo) > 0:
            identifier = project["identifier"]
            if not check_file_in_repository(identifier, "README") \
               and not check_file_in_repository(identifier, "README.txt") \
               and not check_file_in_repository(identifier, "README.md"):
                print "No README or README.txt or README.md!"
                passed = 0

            repo = "https://api.github.com/repos/"+github_repo[19:]
            w = urllib.urlopen(repo)
            gh = json.loads(w.read())
            if len(gh) == 1:
                print("Problem locating repository: "+repo)
            else:
                if not known_external_repo(repo):
                    if gh.has_key("has_wiki") and gh["has_wiki"]:
                        print "A wiki is present!"
                    if gh.has_key("has_issues") and gh["has_issues"]:
                        print "Issues are present!"
                    passed = 0
                    

            

    
print
if  passed == 0:
    print "    ****   FAILURE!   ****"
else:
    print "    ****   SUCCESS!   ****"
    
print
