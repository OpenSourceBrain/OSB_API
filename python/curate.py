'''
Some quality assurance tests on OSB/GitHub repos

Criteria for passing tests are subject to change 

'''   

# TODO:
        
# README & AUTHORS
# Sci Coord, developers, Sci Advisor
# NML statuses
# Simulator statuses
# NML 1/2 native files?
        

import json
import sys

import osb

passed_projects = 0
projects = 0


if __name__ == "__main__":
    
    project_num = 1000
    if len(sys.argv) == 2:
        project_num = int(sys.argv[1])

    for project in osb.get_projects(min_curation_level="Low", limit=project_num):

        print("\n%sProject: %s (%s)\n" % ("-"*8,project.name,project.identifier))

        github_repo = project.github_repo

        if project.is_standard_project() or project.is_showcase():
            projects +=1
            passed = 1

            if project.status == None:
                print("  No status!")
                passed = 0

            if project.is_standard_project():
                if project.spine_classification == None:
                    print("  No spine classification!")
                    passed = 0
                elif not (project.spine_classification == 'Vertebrate' \
                          or project.spine_classification == 'Invertebrate'):
                    print("  Neither vertebrate nor invertebrate!")
                    passed = 0

            if github_repo is not None:
                identifier = project.identifier
                
                if not github_repo.check_file_in_repository("README") \
                   and not github_repo.check_file_in_repository("README.txt") \
                   and not github_repo.check_file_in_repository("README.md"):
                    print("  No README or README.txt or README.md!")
                    passed = 0

                if not osb.known_external_repo(github_repo.full_name):
                    if github_repo.has_wiki:
                        print("  A wiki is present on GitHub!")
                        passed = 0
                    if github_repo.open_issues > 0:
                        print("  (Issues are present on GitHub (%i) - no longer a failing offence...)"%github_repo.open_issues)

            else:
                print("  (No GitHub repository)")

            passed_projects += passed 
            if passed:
                print("  (All checks passed)")

        else:
            print("  (Ignoring, as it is category: %s)"%project.category)



    print("\nNumber of standard/showcase projects: %i, of which %i pass all tests\n"%(projects, passed_projects))

