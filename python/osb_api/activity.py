'''
Some quality assurance tests on OSB/GitHub repos

'''

import json

from __init__ import get_project_list, check_file_in_repository, get_page, get_custom_field

projects = 0
no_status = 0
with_issues = 0
with_wiki = 0
with_forks = 0
with_watchers = 0

for project in get_project_list(limit=1000):
    print "%s\tProject: %s (%s)\n" % ("-"*8,project["name"],project["identifier"])

    projects+=1
    
    github_repo = get_custom_field(project, 'GitHub repository')
    if github_repo!=None and github_repo.endswith(".git"):
         github_repo = github_repo[:-4]
         
    status = get_custom_field(project, 'Status info')
    
    #category = get_custom_field(project, 'Category')
    #spine  = get_custom_field(project, 'Spine classification')
    

    if  status == None or len(status)==0:
        print "No status!"
        no_status+=1


    if github_repo is not None and len(github_repo) > 0:
        identifier = project["identifier"]
        if not check_file_in_repository(identifier, "README") \
           and not check_file_in_repository(identifier, "README.txt") \
           and not check_file_in_repository(identifier, "README.md"):
            print "No README or README.txt or README.md!"
            passed = 0

        repo = "https://api.github.com/repos/"+github_repo[19:]
        print repo
        page = get_page(repo)
        gh = json.loads(page)

        if len(gh) == 1:
            print("Problem locating repository: "+repo)
        else:
            if gh.has_key("has_wiki") and gh["has_wiki"]:
                print "A wiki is present!"
                with_wiki +=1
            if gh.has_key("open_issues") and gh["open_issues"] \
                                         and int(gh["open_issues"])>0:
                print "Issues open: %i"%gh["open_issues"]
                with_issues+=1
            if gh.has_key("forks") and gh["forks"] \
                                   and int(gh["forks"])>0:
                print "Forks: %i"%gh["open_issues"]
                with_forks +=1
            if gh.has_key("watchers") and gh["watchers"] \
                                      and int(gh["watchers"])>0:
                print "Watchers: %i"%gh["watchers"]
                with_watchers+=1

                    

print("\nFound %i projects, %i with no status, %i with wiki, %i with issues, %i with forks, %i with watchers\n"%(projects, no_status, with_wiki, with_issues, with_forks, with_watchers))
