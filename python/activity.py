'''
Some quality assurance tests on OSB/GitHub repos

'''

import json


import osb

import sys

projects = 0

with_issues = 0
num_issues = 0
with_wiki = 0
with_forks = 0
num_forks = 0
with_watchers = 0
num_watchers = 0

if __name__ == "__main__":
    
    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    for project in osb.get_project_list(min_curation_level="None", limit=project_num):

        print("%s\tProject: %s (%s)\n" % ("-"*8,project["name"],project["identifier"]))

        projects+=1

        github_repo = osb.get_custom_field(project, 'GitHub repository')
        if github_repo!=None and github_repo.endswith(".git"):
             github_repo = github_repo[:-4]

        status = osb.get_custom_field(project, 'Status info')

        if github_repo is not None and len(github_repo) > 0:
            identifier = project["identifier"]

            repo = "https://api.github.com/repos/"+github_repo[19:]
            
            page = osb.get_page(repo)
            gh = json.loads(page)

            if len(gh) == 1:
                print("Problem locating repository: "+repo)
            else:
                if gh.has_key("has_wiki") and gh["has_wiki"]:
                    print("A wiki is present!")
                    with_wiki +=1

                if gh.has_key("open_issues") and gh["open_issues"] \
                                             and int(gh["open_issues"])>0:
                    print("Issues open: %i"%gh["open_issues"])
                    with_issues+=1
                    num_issues += int(gh["open_issues"])

                if gh.has_key("forks") and gh["forks"] \
                                       and int(gh["forks"])>0:
                    print("Forks: %i"%gh["forks"])
                    with_forks +=1
                    num_forks += int(gh["forks"])

                if gh.has_key("watchers") and gh["watchers"] \
                                          and int(gh["watchers"])>0:
                    print("Watchers: %i"%gh["watchers"])
                    with_watchers+=1
                    num_watchers += int(gh["watchers"])



    print("\nFound %i projects, %i with wiki, %i with issues (%i total), %i with forks (%i total), %i with watchers (%i total)\n" % \
             (projects, with_wiki, with_issues, num_issues, with_forks, num_forks, with_watchers, num_watchers))
