'''
Script to check ModelDB references
'''


import osb
import operator

projects = 0
with_tags = 0
tags = {}

min_curation_level="Low"
    
for project in osb.get_projects(min_curation_level):

    if project.is_standard_project() or project.is_showcase():
        
        print("\n--------   Project: %s: %s\n" % (project.identifier,project.name))
        projects+=1
        
        if project.tags:
            print("    Project has tags: %s" % (project.tags))
            with_tags +=1
            for tag in project.tags:
                if not tag in tags:
                    tags[tag] = 0
                tags[tag] +=1
    

print("\nThere were %i projects (min_curation_level=%s), %i of which had tags\n"%(projects, min_curation_level, with_tags))
sorted_tags = sorted(tags.items(), key=operator.itemgetter(1), reverse=True)
for s in sorted_tags:
    print("%s: %s %i projects"%(s[0], " "*(50-len(s[0])), s[1]))
        
