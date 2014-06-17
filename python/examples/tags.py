'''
Script to check ModelDB references
'''


import osb
import operator

projects = 0
with_tags = 0
tags = {}
    
for project in osb.get_projects(min_curation_level="Low"):

    if project.is_standard_project() or project.is_showcase():
        
        print "\n--------   Project: %s\n" % project.name
        projects+=1

        if project.tags:
            print "    Project has tags: %s" % (project.tags)
            with_tags +=1
            for tag in project.tags:
                if not tags.has_key(tag):
                    tags[tag] = 0
                tags[tag] +=1
    

print("\nThere were %i projects, %i of which had tags\n"%(projects, with_tags))
sorted_tags = sorted(tags.iteritems(), key=operator.itemgetter(1), reverse=True)
for s in sorted_tags:
    print("%s: %s %i projects"%(s[0], " "*(50-len(s[0])), s[1]))
        
