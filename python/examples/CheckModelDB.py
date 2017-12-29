'''
Script to check ModelDB references
'''


import osb

projects = 0
with_modeldb = 0
    
for project in osb.get_projects(min_curation_level="None"):

    if project.is_standard_project():
        
        print("\n--------   Project: %s\n" % project.name)
        projects+=1

        if project.modeldb_reference and project.modeldb_reference != 'None':
            print("    OSB link:%shttp://opensourcebrain.org/projects/%s" % (" "*22, project.identifier))
            print("    ModelDB link:%shttp://senselab.med.yale.edu/ModelDB/ShowModel?model=%s" % (' '*18, project.modeldb_reference))
            with_modeldb +=1
        else:
            print("    No ModelDB info for model")
    

print("\nThere were %i projects, %i of which had ModelDB information\n"%(projects, with_modeldb))
        
