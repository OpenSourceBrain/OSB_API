'''
Script to check ModelDB references
'''


from __init__ import get_project_list, get_custom_field, print_custom_field

projects = 0
with_modeldb = 0
    
for project in get_project_list():

    isProj = get_custom_field(project, 'Category') == 'Project'
    mdb = get_custom_field(project, 'ModelDB reference')
    hasMDB = mdb != None and len(mdb)>0
    
    
    if isProj:
        print "\n--------   Project: %s\n" % project["name"]
        projects+=1

        if hasMDB:
            print "    OSB link:%shttp://opensourcebrain.org/projects/%s" % \
                                                (" "*22,project["identifier"])
            print_custom_field(project, 'ModelDB reference')
            with_modeldb +=1
        else:
            print "    No ModelDB info for model"
    

print("\nThere were %i projects, %i of which had ModelDB information\n"%(projects, with_modeldb))
        
