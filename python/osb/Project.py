from OSBEntity import OSBEntity

from __init__ import *
from Repository import *

class Project(OSBEntity):
    
    IDENTIFIER = 'identifier'
    NAME = 'name'
    ID = 'id'
    DESCRIPTION = 'description'
    CREATED_ON = 'created_on'
    UPDATED_ON = 'updated_on'
    
    CATEGORY = 'Category'
    CATEGORY_ATTR = 'category'
    CATEGORY_OSB = 'OSB'
    CATEGORY_PROJECT = 'Project'
    CATEGORY_SHOWCASE = 'Showcase'
    CATEGORY_GUIDE = 'Guide'
    CATEGORY_THEME = 'Theme'
    
    MODELDB_REFERENCE = 'ModelDB reference'
    MODELDB_REFERENCE_ATTR = 'modeldb_reference'
    
    GITHUB_REPO_CF = "GitHub repository"
    GITHUB_REPO_ATTR = "github_repo_str"
    
    GITHUB_REPO_OBJ = "github_repo"
    
    STATUS = 'Status info'
    STATUS_ATTR = 'status'
    
    SPECIES = 'Specie'
    SPECIE_ATTR = 'specie'
    SPECIES_ATTR = 'species'
    
    BRAIN_REGION = "Brain region"
    BRAIN_REGION_ATTR = "brain_region"
    
    
    def __init__(self, info_array):
        OSBEntity.__init__(self, info_array)
    
    def __getattr__(self, name):
        #print("Checking for attr %s..."%(name))
        #print self.info_array.keys()
        if name == self.IDENTIFIER:
            return self.info_array[self.IDENTIFIER]
        elif name == self.NAME:
            return self.info_array[self.NAME]
        elif name == self.ID:
            return self.info_array[self.ID]
        elif name == self.DESCRIPTION:
            return self.info_array[self.DESCRIPTION]
        elif name == self.CREATED_ON:
            return self.info_array[self.CREATED_ON]
        elif name == self.UPDATED_ON:
            return self.info_array[self.UPDATED_ON]
        
        elif name == self.CATEGORY_ATTR:
            return self.get_custom_field(self.CATEGORY)
        
        elif name == self.MODELDB_REFERENCE_ATTR:
            return self.get_custom_field(self.MODELDB_REFERENCE)
        
        elif name == self.GITHUB_REPO_ATTR:
            return self.get_custom_field(self.GITHUB_REPO_CF)
        
        elif name == self.GITHUB_REPO_OBJ:
            repo = self.get_custom_field(self.GITHUB_REPO_CF)
            if repo:
                ghr = GitHubRepository.create(repo)
                return ghr
            else:
                return None
        
        elif name == self.STATUS_ATTR:
            return self.get_custom_field(self.STATUS)
        
        elif name == self.SPECIE_ATTR or name == self.SPECIES_ATTR:
            return self.get_custom_field(self.SPECIES)
        
        elif name == self.BRAIN_REGION_ATTR:
            return self.get_custom_field(self.BRAIN_REGION)
        
        else: 
            print("-- Could not find attribute: %s"%name)
            return None
        
    def __getitem__(self, name):
        #print("Checking for item %s..."%(name))
        return None
        
    def __str__(self):
        return "OSB Project: %s (%s)"%(self.name, self.identifier)
        
    def is_standard_project(self):
        return self.category == self.CATEGORY_PROJECT
    
    def is_showcase(self):
        return self.category == self.CATEGORY_SHOWCASE
    
        
        
if __name__ == "__main__":

    project_array = get_project('grancelllayer')
    
    project = Project(project_array)
    print project.id
    
    #print("Project %s, %s: %s"%(project.id, project.identifier, project.name))
    #print("Category: %s (Standard project? %s)"%(project.category, project.is_standard_project()))
    #print("ModelDB reference: %s"%(project.modeldb_reference))
    #print("GitHub repo: %s"%(project.github_repo_str))
    
    print("Done")