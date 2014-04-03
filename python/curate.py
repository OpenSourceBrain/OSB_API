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

    for project in osb.get_project_list(min_curation_level="Low", limit=project_num):

        print "%sProject: %s (%s)\n" % ("-"*8,project["name"],project["identifier"])

        github_repo = osb.get_custom_field(project, 'GitHub repository')
        if github_repo!=None and github_repo.endswith(".git"):
             github_repo = github_repo[:-4]

        status = osb.get_custom_field(project, 'Status info')

        category = osb.get_custom_field(project, 'Category')
        spine  = osb.get_custom_field(project, 'Spine classification')


        if category == "Project" or category == "Showcase":
            projects +=1
            passed = 1

            if status == None or len(status)==0:
                print "  No status!"
                passed = 0

            if category == "Project":
                if spine == None or len(spine)==0:
                    print "  No spine classification!"
                    passed = 0
                elif not (spine == 'Vertebrate' or spine == 'Invertebrate'):
                    print "  Neither vertebrate nor invertebrate!"
                    passed = 0

            if github_repo is not None and len(github_repo) > 0:
                identifier = project["identifier"]
                if not osb.check_file_in_repository(identifier, "README") \
                   and not osb.check_file_in_repository(identifier, "README.txt") \
                   and not osb.check_file_in_repository(identifier, "README.md"):
                    print "  No README or README.txt or README.md!"
                    passed = 0

                repo = "https://api.github.com/repos/"+github_repo[19:]
                page = osb.get_page(repo)
                gh = json.loads(page)
                if len(gh) == 1:
                    print("  Problem locating repository: "+repo)
                else:
                    if not osb.known_external_repo(repo):
                        if gh.has_key("has_wiki") and gh["has_wiki"]:
                            print "  A wiki is present on GitHub!"
                            passed = 0
                        if gh.has_key("has_issues") and gh["has_issues"]:
                            print "  (Issues are present on GitHub - no longer a failing offence...)"

            else:
                print("  (No GitHub repository)")

            passed_projects += passed   

        else:
            print("  (Ignoring, as it is category: %s)"%category)



    print("\nNumber of standard/showcase projects: %i, of which %i pass all tests\n"%(projects, passed_projects))

