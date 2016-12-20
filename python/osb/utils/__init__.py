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

from osb import get_github_auth, github_auth_info

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
    t.write(str(f.read().decode("utf-8")))
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


def get_page(url, username=None, password=None, utf8=False):
    if 'api.github.com' in url:
        url = url.replace('/tree/master/neuroConstruct', '')
        # This cruft was in some of the urls. 
    
    if 'github' in url:
        
        GITHUB_USERNAME, GITHUB_PASSWORD = get_github_auth()
        if username is None:
            username = GITHUB_USERNAME
        if password is None:
            password = GITHUB_PASSWORD

    result = ""
    #print(">>> Getting URL: %s (username=%s)" % (url, username))
    req = Request(url)
    if username and password:
        unamepw = bytearray('%s:%s' % (username, password), 'utf-8')
        auth = base64.urlsafe_b64encode(unamepw)
        req.add_header("Authorization", "Basic %s" % str(auth.decode("utf-8")))
        #req.add_header("Content-Type", "application/json")
        #req.add_header("Accept", "application/json")
    try:
        response = urlopen(req)
    except HTTPError as e:
        print("URL: %s produced error %d (%s)" % (url, e.code, e.msg))
        print("Request: (%s)" % (req.headers))
        if e.code != 404:
            print(github_auth_info)
    else:
        read_resp = response.read()
        if utf8:
            try:
                result = str(read_resp.decode("utf-8"))
            except Exception as e:
                print("Error converting response to utf-8. Original response from: %s:"%url)
                print("=====================================================")
                print(read_resp)
                print("=====================================================")
                print(e)
        else:
            result = read_resp
    #print(">>> Returning: [[%s]]..."%result[0: min(len(result), 40)])
    return result
