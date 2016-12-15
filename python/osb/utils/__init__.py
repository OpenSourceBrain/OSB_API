"""
Methods useful for all test scripts.

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

from .. import USERNAME,PASSWORD

LEMS_SUFFIX = ".xml"
LEMS_PREFIX1 = "Run_"
LEMS_PREFIX2 = "LEMS_"
NML2_SUFFIX = ".nml"


def check_jnml_validates_neuroml(document):
    p = subprocess.Popen(["jnml -validate " + document], 
                         shell=True, 
                         stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode


def is_lems_file(file):
    return file.endswith(LEMS_SUFFIX) and (file.startswith(LEMS_PREFIX1) or file.startswith(LEMS_PREFIX2))


def is_nml2_file(file):
    return file.endswith(NML2_SUFFIX)


def check_jnml_loads_lems(document):
    p = subprocess.Popen(["jnml " + document + " -norun"], 
                         shell=True, 
                         stdout=subprocess.PIPE)
    p.communicate()
    return p.returncode


def get_custom_field(project_array, cfName):
    result = None
    for cf in project_array["custom_fields"]:
        if cf['name'] == cfName and 'value' in cf:
            result = cf['value']
    return result


def copy_file_from_url(url_file, target_file):
    #print("copy_file_from_url: %s, %s"%(url_file, target_file))
    f = urlopen(url_file)
    if '/' in target_file:
        parent_dir = target_file[:target_file.rfind('/')]
        check_exists_dir_and_children(parent_dir)

    t = open(target_file, 'w')
    t.write(f.read())
    print("  ...Downloaded: " + target_file)


def check_exists_dir_and_children(file):
    #print("check_exists_dir_and_children: %s"%file)
    if os.path.exists(file): return
    if '/' in file:
        parent_dir = file[:file.rfind('/')]
        check_exists_dir_and_children(parent_dir)
    if not os.path.exists(file):
        os.makedirs(file)


def build_request(url):
    if not self.is_authenticated:
        return Request(url)
    auth = {'Authorization': 'token %s' % (self.token)}
    return Request(url, auth)


def get_page(url, username=None, password=None):
    if 'api.github.com' in url:
        url = url.replace('/tree/master/neuroConstruct', '')
        # This cruft was in some of the urls. 
    
    if 'github' in url:
        if username is None:
            username = USERNAME
        if password is None:
            password = PASSWORD

    result = ""
    #print(">>> Getting URL: %s (username=%s)" % (url, username))
    req = Request(url)
    if username and password:
        unamepw = "%s:%s" % (username, password)
        auth = base64.urlsafe_b64encode(unamepw)
        req.add_header("Authorization", "Basic %s" % auth)
        #req.add_header("Content-Type", "application/json")
        #req.add_header("Accept", "application/json")
    try:
        response = urlopen(req)
    except HTTPError as e:
        print("URL: %s produced error %d (%s)" % (url, e.code, e.msg))
        if e.code != 404:
            print(auth_info)
    else:
        result = response.read()
    #print(">>> Returning: %s..."%result[0: min(len(result), 20)])
    return result
