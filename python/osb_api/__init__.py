"""
Functions shared by all test scripts.
Call any script with no arguments to skip (GitHub) authentication, e.g.:
python osb_api/curate.py
Call with commandline arguments to enable (GitHub) authentication, e.g.:
python osb_api/curate.py username:YOUR_USERNAME and password:YOUR_PASSWORD

"""

import sys
import urllib
import urllib2
import base64
import json

USERNAME = None
PASSWORD = None

for arg in sys.argv[1:]:
    try:
        key,value = arg.split(":")
    except ValueError,e:
        print "Command line argument %s had error %s" % (arg,e.strerror)
    else:
        if key == "username":            
            USERNAME = value
        if key == "password":
            PASSWORD = value

def get_project_list(limit=1000):
    url = "http://www.opensourcebrain.org/projects.json"
    page = get_page('%s?limit=%d' % (url,limit))
    json_data = json.loads(page)
    project_list = json_data['projects']
    return project_list

def get_project(project_identifier,project_list=None):
    if project_list is None:
        project_list = get_project_list()
    project = None
    for candidate_project in project_list:
        if candidate_project['identifier'] == project_identifier:
            project = candidate_project
            break
    if project is None:
        print "No project found with identifier %s" % project_identifier
    return project

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
    page = get_page(rest_url)
    json_files = json.loads(page)
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

def build_request(url):
    if not self.is_authenticated:
        return Request(url)
    auth = {'Authorization': 'token %s' % (self.token)}
    return Request(url, auth)

def get_page(url,username=None,password=None):
    if 'api.github.com' in url:
        url = url.replace('/tree/master/neuroConstruct','')
        # This cruft was in some of the urls.  
    request = urllib2.Request(url)
    if username is None:
        username = USERNAME
    if password is None:
        password = PASSWORD
    
    result = ""
    req = urllib2.Request(url)
    if username and password:
        auth = base64.urlsafe_b64encode("%s:%s" % (username, password))
        req.add_header("Authorization", "Basic %s" % auth)
        #req.add_header("Content-Type", "application/json")
        #req.add_header("Accept", "application/json")
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print "URL: %s produced error %d (%s)" % (url,e.code,e.msg)
    else:
        result = response.read()
    return result
