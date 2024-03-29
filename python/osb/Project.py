
from osb.OSBEntity import OSBEntity
from osb.Repository import GitHubRepository
from osb.utils import get_page

import json

class Project(OSBEntity):

    attrs = {
        'IDENTIFIER': 'identifier',
        'NAME': 'name',
        'ID': 'id',
        'DESCRIPTION': 'description',
        'CREATED_ON': 'created_on',
        'UPDATED_ON': 'updated_on',

        'CATEGORY': 'Category',

        'TAGS': 'Tags',

        'MODELDB_REFERENCE': 'ModelDB reference',

        'GITHUB_REPO_ATTR': "GitHub repository",
        'GITHUB_REPO_STR': "GitHub repository",
        'GITHUB_REPO_NAME': "Github repository name",

        'GITHUB_REPO': "github_repo", # Used for GitHubRepository object

        'STATUS': 'Status info',

        'ENDORSEMENT': 'Endorsement',

        'SPECIES': 'Specie',
        'SPECIE': 'specie',

        'BRAIN_REGION': "Brain region",

        'CELL_TYPE': "Cell type",

        'SPINE_CLASSIFICATION': 'Spine classification',

        'NEUROLEX_IDS_CELLS': 'NeuroLex Ids: Cells',
        }

    labels = {
        'CATEGORY_ATTR': 'category',
        'CATEGORY_OSB': 'OSB',
        'CATEGORY_PROJECT': 'Project',
        'CATEGORY_SHOWCASE': 'Showcase',
        'CATEGORY_GUIDE': 'Guide',
        'CATEGORY_THEME': 'Theme',
    }

    def __init__(self, info_array):
        OSBEntity.__init__(self, info_array)

    def __getattr__(self, name):
        #print("Checking for attr %s..."%(name))
        #print self.info_array.keys()
        value = None

        if name in self.labels:
            value = self.labels[name]

        name = name.upper().replace(' ','_').replace(':','')
        #print("Checking for attr %s..."%(name))
        if name in self.attrs:
            attr = self.attrs[name]
            try:
                value = str(self.info_array[attr])
            except:
                value = str(self.get_custom_field(attr))

        if name == 'TAGS':
            value = str(value).split(",") if value is not None else []

        elif name == 'GITHUB_REPO':
            repo_str = self.get_custom_field('GitHub repository')
            #print repo_str
            value = GitHubRepository.create(repo_str)

        elif name == 'GITHUB_REPO_NAME':
            repo_str = self.get_custom_field('GitHub repository')
            if repo_str:
                value = repo_str.split('/')[-1].replace('.git','')
            else:
                value = ''

        #print("  --- value: %s"%str(value))
        if value is None: 
            try:
                value = super(Project,self).__getattr__(name)
            except Exception as e:
                #print e
                #print("  --- Could not find attribute in Project: %s"%name)
                pass

        try:
            v = float(value)
            if v == int(v):
                return int(v)
            else:
                return v
        except ValueError:
            return value
        except TypeError:
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
        url = "https://v1.opensourcebrain.org/projects/%s.json"%project_identifier
        page = get_page('%s' % (url), utf8=True)
        json_data = json.loads(page)
        if 'project' in json_data:
            result = json_data['project']
        if result is None:
            print("No project with identifier %s" % project_identifier)
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
                        print("Using project with similar identifier %s" \
                                            % c)
                        result = cls.get_data(c)
                        break
        return result

    @classmethod
    def get(cls, project_identifier, fuzzy=False):
        project_data = cls.get_data(project_identifier, fuzzy=fuzzy)
        return cls(project_data)


if __name__ == "__main__":

    project_names = ['thalamocortical',
                     'balanced-plastic-networks',
                     'alleninstituteneuroml']
    
    for pn in project_names:
        project = Project.get(pn)

        print("Project %s, %s: %s"%(project.id, project.identifier, project.name))
        print("Category: %s (Standard project? %s)"%(project.category, project.is_standard_project()))
        print("ModelDB reference: %s"%(project.modeldb_reference))
        print("Endorsement: %i"%(project.endorsement==1))
        print("GitHub repo str: %s"%(project.github_repo_str))
        print("GitHub repo: %s"%(project.github_repo))
        print("Tags: %s"%(project.tags))
        print("----------------------------------------")

    print("Done")
