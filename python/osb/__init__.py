"""
Functions shared by all test scripts.
Call any script with no arguments to skip (GitHub) authentication, e.g.:
python osb_api/curate.py
Call with commandline arguments to enable (GitHub) authentication, e.g.:
python osb_api/curate.py username:YOUR_USERNAME and password:YOUR_PASSWORD

"""

import sys

try:
    from urllib2 import urlopen, HTTPError, Request  # Python 2
except:
    from urllib.request import urlopen, HTTPError, Request # Python 3

import base64
import json
import os.path
import subprocess

from Project import *

USERNAME = None
PASSWORD = None
auth_file = "github.info"

for arg in sys.argv[1:]:
    try:
        key,value = arg.split(":")
        if key == "username":            
            USERNAME = value
        if key == "password":
            PASSWORD = value
    except ValueError as e:
        ignored_arg = arg

if os.path.isfile(auth_file):
    for line in open(auth_file, 'r'):
        if line.startswith("username:"):
            USERNAME = line.strip()[9:]
        if line.startswith("password:"):
            PASSWORD = line.strip()[9:]
            
            
    
def list_files_in_repo(gh_repo):
    #rest_url = "https://api.github.com/repos/%s/contents/%s"%(gh_repo, dirname)
    # GET /repos/:owner/:repo/git/trees/:sha
    rest_url = "https://api.github.com/repos/%s/git/trees/master?recursive=1"%(gh_repo)
    print("URL: %s"%rest_url)
    w = urlopen(rest_url)
    json_files = json.loads(w.read())
    if not json_files.has_key('tree'):
        print("Error!")
        print(json_files)
    files = []
    tree = json_files["tree"]
    for entry in tree:
        files.append(entry["path"])
    return files

        

def get_project_list(min_curation_level, limit=1000):
    url = "http://www.opensourcebrain.org/projects.json"
    page = get_page('%s?limit=%d' % (url,limit))
    json_data = json.loads(page)
    project_list_all = json_data['projects']
    project_list = []
    for project in project_list_all:

        curation_level = int(get_custom_field(project, "Curation level")) if get_custom_field(project, "Curation level") else 0
        
        if (min_curation_level=="None") or \
           (min_curation_level=="Low" and curation_level>=1)  or \
           (min_curation_level=="Medium" and curation_level>=2)  or \
           (min_curation_level=="High" and curation_level>=3):
            project_list.append(project)
            
    return project_list

def get_projects(min_curation_level, limit=1000):
    url = "http://www.opensourcebrain.org/projects.json"
    page = get_page('%s?limit=%d' % (url,limit))
    json_data = json.loads(page)
    project_list_all = json_data['projects']
    projects = []
    for project in project_list_all:

        curation_level = int(get_custom_field(project, "Curation level")) if get_custom_field(project, "Curation level") else 0
        
        if (min_curation_level=="None") or \
           (min_curation_level=="Low" and curation_level>=1)  or \
           (min_curation_level=="Medium" and curation_level>=2)  or \
           (min_curation_level=="High" and curation_level>=3):
            projects.append(Project(project))
            
    return projects

def get_project(project_identifier,project_list=None):
    if project_list is None:
        project_list = get_projects(min_curation_level="None")
    project = None
    for candidate_project in project_list:
        if candidate_project.identifier == project_identifier:
            project = candidate_project
            break
    if project is None:
        print("No project found with identifier %s" % project_identifier)
    return project

def check_file_in_repository(projectId, filename):
    
    try:
        urlopen("http://www.opensourcebrain.org/projects/%s/repository/changes/%s" % (projectId, filename))
        return True
    except HTTPError:
        return False

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
        print("%sModelDB link:%shttp://senselab.med.yale.edu/ModelDB/ShowModel.asp?model=%s" % (' '*4,' '*18,value))
    elif value is not None:
        print("%s%s:%s%s" % (' '*4,cfName,' '*13,value))

def get_cell_neurolex_ids(project):
    return get_custom_field(project,'NeuroLex Ids: Cells')

def list_files_in_repo_dir(gh_repo, dirname):
    rest_url = "https://api.github.com/repos/%s/contents/%s"%(gh_repo, dirname)
    page = get_page(rest_url)
    json_files = json.loads(page)
    files = []
    for entry in json_files:
        files.append(entry["name"])
    return files


def copy_file_from_url(url_file, target_file):
    #print("copy_file_from_url: %s, %s"%(url_file, target_file))
    f = urlopen(url_file)
    if '/' in target_file:
        parent_dir = target_file[:target_file.rfind('/')]
        check_exists_dir_and_children(parent_dir)
    
    t = open(target_file, 'w')
    t.write(f.read())
    print("Downloaded: "+target_file)

def check_exists_dir_and_children(file):
    #print("check_exists_dir_and_children: %s"%file)
    if os.path.exists(file): return
    if '/' in file:
        parent_dir = file[:file.rfind('/')]
        check_exists_dir_and_children(parent_dir)
    if not os.path.exists(file):
        os.makedirs(file)

def check_jnml_validates_neuroml(document):
    p = subprocess.Popen(["jnml -validate "+ document], 
                          shell=True, 
                          stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode


lems_suffix = ".xml"
lems_prefix1 = "Run_"
lems_prefix2 = "LEMS_"

def is_lems_file(file):
    return file.endswith(lems_suffix) and (file.startswith(lems_prefix1) or file.startswith(lems_prefix2))


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
    request = Request(url)
    if username is None:
        username = USERNAME
    if password is None:
        password = PASSWORD
    
    result = ""
    req = Request(url)
    if username and password:
        auth = base64.urlsafe_b64encode("%s:%s" % (username, password))
        req.add_header("Authorization", "Basic %s" % auth)
        #req.add_header("Content-Type", "application/json")
        #req.add_header("Accept", "application/json")
    try:
        response = urlopen(req)
    except HTTPError as e:
        print("URL: %s produced error %d (%s)" % (url,e.code,e.msg))
    else:
        result = response.read()
    return result
