"""
Main helper methods for accessing OSB API

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

GITHUB_USERNAME = None
GITHUB_PASSWORD = None

github_auth_file = "github.info"

github_auth_info = "\n-----------------------------------------------------------------\n\n"+\
            "  GitHub limits the number of calls to its API for unauthorised users (~60 per hour).\n"+\
            "  For registered GitHub users, this goes up to ~5000 per hour. To use your GitHub account\n"+\
            "  details, either create a file "+github_auth_file+" containing the lines:\n\n    username:YOUR_USERNAME\n    password:YOUR_PASSWORD\n\n"+\
            "  or call with commandline arguments, e.g.:\n"+\
            "\n    python curate.py username:YOUR_USERNAME and password:YOUR_PASSWORD\n\n"+\
            "\n\n    Remember too, if you have 2 stage authentication you'll have to generate a new token as your password.\n\n"+\
            "-----------------------------------------------------------------"
            


for arg in sys.argv[1:]:
    try:
        key,value = arg.split(":")
        if key == "username":            
            GITHUB_USERNAME = value
        if key == "password":
            GITHUB_PASSWORD = value
    except ValueError as e:
        ignored_arg = arg

if os.path.isfile(github_auth_file):
    for line in open(github_auth_file, 'r'):
        if line.startswith("username:"):
            GITHUB_USERNAME = line.strip()[9:]
        if line.startswith("password:"):
            GITHUB_PASSWORD = line.strip()[9:]
            
def get_github_auth():
    return GITHUB_USERNAME, GITHUB_PASSWORD

from osb.utils import get_page, get_custom_field
from osb.Project import Project

def get_projects_data(min_curation_level, limit=1000):
    url = "http://www.opensourcebrain.org/projects.json"
    page = get_page('%s?limit=%d' % (url,limit)).decode('utf-8')
    json_data = json.loads(page)
    projects_data_all = json_data['projects']
    projects_data = []
    for project_data in projects_data_all:
        
        curation_level = 0
        text = "Curation level"
        if get_custom_field(project_data, text):
            curation_level = int(get_custom_field(project_data, text)) 
        
        if (min_curation_level in ["None",None,"",0]) or \
           (min_curation_level in ["Low",1] and curation_level>=1)  or \
           (min_curation_level in ["Medium",2] and curation_level>=2)  or \
           (min_curation_level in ["High",3] and curation_level>=3):
            projects_data.append(project_data)
            
    return projects_data

def get_projects(min_curation_level, limit=1000):
    projects_data = get_projects_data(min_curation_level, limit=limit)
    projects = [Project(project_data) for project_data in projects_data]
    return projects

def get_projects_identifiers(min_curation_level, limit=1000):
    projects = get_projects(min_curation_level, limit=limit)
    projects_identifiers = [project.identifier for project in projects]
    return projects_identifiers

def get_project_with_identifier(identifier,projects=None):
    if projects is None:
        projects = get_projects(None)
    result = None
    identifier = identifier.lower()
    for project in projects:
        if identifier in [project.identifier.lower(),
                          project.GITHUB_REPO_NAME.lower()]:
            result = project
            break
    return result 

def known_external_repo(reponame):
    if "openworm" in reponame or \
       "neuralgorithm" in reponame or \
       "Simon-at-Ely" in reponame:
        return True
    else:
        return False
