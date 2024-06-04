'''
Some quality assurance tests on OSB/GitHub repos

'''

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

from retrieveNML2 import ignores

if __name__ == "__main__":
    
    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    for project in osb.get_projects(min_curation_level="Low", limit=project_num):
        
        print("\n%s\tProject: %s (%s)\n" % ("-"*8, project.name, project.identifier))
        
        if project.identifier in ignores:
            print("Ignoring...")
            
        else:
            
            projects+=1

            github_repo = project.github_repo

            if github_repo is not None:

                if github_repo.has_wiki:
                    print("  A wiki is present!")
                    with_wiki +=1

                if github_repo.open_issues > 0:
                    print("  Issues open: %i" % github_repo.open_issues)
                    with_issues+=1
                    num_issues += github_repo.open_issues

                if github_repo.forks > 0:
                    print("  Forks: %i" % github_repo.forks)
                    with_forks +=1
                    num_forks += github_repo.forks

                if github_repo.watchers > 0:
                    print("  Watchers: %i"%github_repo.watchers)
                    with_watchers+=1
                    num_watchers += github_repo.watchers



    print("\nFound %i projects, %i with wiki, %i with issues (%i total), %i with forks (%i total), %i with watchers (%i total)\n" % \
             (projects, with_wiki, with_issues, num_issues, with_forks, num_forks, with_watchers, num_watchers))
