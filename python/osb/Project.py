from OSBEntity import OSBEntity

from __init__ import *
from Repository import *

class Project(OSBEntity):
    
    attrs = {
        'IDENTIFIER': 'identifier',
        'NAME': 'name',
        'ID': 'id',
        'DESCRIPTION': 'description',
        'CREATED_ON': 'created_on',
        'UPDATED_ON': 'updated_on',
    
        'CATEGORY': 'Category',
        'CATEGORY_ATTR': 'category',
        'CATEGORY_OSB': 'OSB',
        'CATEGORY_PROJECT': 'Project',
        'CATEGORY_SHOWCASE': 'Showcase',
        'CATEGORY_GUIDE': 'Guide',
        'CATEGORY_THEME': 'Theme',
    
        'TAGS': 'Tags',

        'MODELDB_REFERENCE': 'ModelDB reference',
        
        'GITHUB_REPO_ATTR': "GitHub repository",
        'GITHUB_REPO_OBJ': "GitHub repository",
    
        'STATUS': 'Status info',
        
        'ENDORSEMENT': 'Endorsement',
        
        'SPECIES': 'Specie',
        'SPECIE': 'specie',
        
        'BRAIN_REGION': "Brain region",
        
        'CELL_TYPE': "Cell type",
        
        'SPINE_CLASSIFICATION': 'Spine classification',
        
        'NEUROLEX_IDS_CELLS': 'NeuroLex Ids: Cells',
        }

    def __init__(self, info_array):
        OSBEntity.__init__(self, info_array)
    
    def __getattr__(self, name):
        #print("Checking for attr %s..."%(name))
        #print self.info_array.keys()
        value = None

        name = name.upper().replace(' ','_').replace(':','')
        if name in self.attrs:
            attr = self.attrs[name]
            try:
                value = self.info_array[attr]
            except:
                value = self.get_custom_field(attr)

        if name == 'TAGS':
            value = str(value).split(",") if value is not None else []
        
        elif name == 'GITHUB_REPO_OBJ':
            if value: # A repository.  
                value = GitHubRepository.create(value)
            else:
                value = None
        
        if value is None: 
            try:
                value = super(Project,self).__getattr__(name)
            except:
                #print("-- Could not find attribute: %s"%name)
                pass

        return value
        
    def __getitem__(self, name):
        #print("Checking for item %s..."%(name))
        return None
        
    def __str__(self):
        return "OSB Project: %s (%s)"%(self.name, self.identifier)
        
    def is_standard_project(self):
        return self.category == self.CATEGORY_PROJECT
    
    def is_showcase(self):
        return self.category == self.CATEGORY_SHOWCASE
    
    @classmethod
    def get_data(cls, project_identifier, fuzzy=False):
        result = None
        url = "http://www.opensourcebrain.org/projects/%s.json"%project_identifier
        page = utils.get_page('%s' % (url))
        json_data = json.loads(page)
        if 'project' in json_data:
            result = json_data['project']
        if result is None:
            print "No project with identifier %s" % project_identifier
            if fuzzy:
                projects_identifiers = get_projects_identifiers()
                for candidate_project_identifier in projects_identifiers:
                    p = project_identifier.lower()
                    c = candidate_project_identifier
                    match = (p in c) or (c in p) or \
                            (p.replace('-','') in c) or \
                            (c in p.replace('-','')) or \
                            (p.replace('_','') in c) or \
                            (c in p.replace('_',''))
                    if match:
                        print "Using project with similar identifier %s" \
                                            % c
                        result = cls.get_data(c)
                        break
        return result

    @classmethod
    def get(cls, project_identifier, fuzzy=False):
        project_data = cls.get_data(project_identifier, fuzzy=fuzzy)
        return cls(project_data)
    
        
if __name__ == "__main__":
   
    project = Project.get('grancelllayer')
    print project.id
    
    #print("Project %s, %s: %s"%(project.id, project.identifier, project.name))
    #print("Category: %s (Standard project? %s)"%(project.category, project.is_standard_project()))
    #print("ModelDB reference: %s"%(project.modeldb_reference))
    #print("GitHub repo: %s"%(project.github_repo_str))
    
    print("Done")