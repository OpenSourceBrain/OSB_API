"""Functions shared by all test scripts."""

import urllib

def check_file_in_repository(projectId, filename):
    f = urllib.urlopen("http://www.opensourcebrain.org/projects/%s/repository/changes/%s" % (projectId, filename))
    if "The entry or revision was not found in the repository" in f.read():
        return False
    else:
        return True

def known_external_repo(reponame):
    if "openworm" in reponame or \
       "neuralgorithm" in reponame or \
       "Simon-at-Ely" in reponame:
        return True
    else:
        return False

def get_custom_field(project, cfName):
    result = None
    for cf in project["custom_fields"]:
        if cf['name'] == cfName and cf.has_key('value'):  
            result = cf['value']
    return result

def print_custom_field(project, cfName):
    value = get_custom_field(project,cfName)
    if value == 'ModelDB reference':
        print "%sModelDB link:%shttp://senselab.med.yale.edu/ModelDB/ShowModel.asp?model=%s" % (' '*4,' '*18,value)
    elif value is not None:
        print "%s%s:%s%s" % (' '*4,cfName,' '*13,value)

def get_cell_neurolex_ids(project):
    return get_custom_field(project,'NeuroLex Ids: Cells')

def list_files_in_repo_dir(gh_repo, dirname):
    rest_url = "https://api.github.com/repos/%s/contents/%s"%(gh_repo, dirname)
    w = urllib.urlopen(rest_url)
    json_files = json.loads(w.read())
    files = []
    for entry in json_files:
        #print entry
        files.append(entry["name"])
    return files

def copy_file_from_url(url_file, target_file):
    f = urllib.urlopen(url_file)
    t = open(target_file, 'w')
    t.write(f.read())
    print "Created: "+target_file,

def check_jnml_validates_NeuroML(document):
    p = subprocess.Popen(["jnml -validate "+ document], 
                          shell=True, 
                          stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode

def check_jnml_loads_lems(document):
    p = subprocess.Popen(["jnml "+ document+ " -norun"], 
                          shell=True, 
                          stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode

