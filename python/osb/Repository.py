
from osb import HTTPError, urlopen
from osb.utils import get_page, copy_file_from_url

import json

class Repository():

    type = "???"

    NAME = 'name'
    FULL_NAME = 'full_name'
    URL = 'url'
    HTML_URL = 'html_url'
    CLONE_URL = 'clone_url'
    HAS_WIKI = 'has_wiki'
    OPEN_ISSUES = 'open_issues'
    FORKS = 'forks'
    WATCHERS = 'watchers'

    def __init__(self, info_array, type, check_file_template, list_files_template):
        self.type = type
        self.info_array = info_array
        self.check_file_template = check_file_template
        self.list_files_template = list_files_template


    def __getattr__(self, name):

        if name == self.NAME:
            return self.info_array[self.NAME]

        elif name == self.FULL_NAME:
            return self.info_array[self.FULL_NAME]

        elif name == self.URL:
            return self.info_array[self.URL]

        elif name == self.HTML_URL:
            return self.info_array[self.HTML_URL]

        elif name == self.CLONE_URL:
            return self.info_array[self.CLONE_URL]

        elif name == self.OPEN_ISSUES:
            oi = self.info_array[self.OPEN_ISSUES]
            if oi is not None:
                return int(oi)
            else:
                return 0

        elif name == self.HAS_WIKI:
            return self.info_array[self.HAS_WIKI]

        elif name == self.FORKS:
            f = self.info_array[self.FORKS]
            if f is not None:
                return int(f)
            else:
                return 0

        elif name == self.WATCHERS:
            w = self.info_array[self.WATCHERS]
            if w is not None:
                return int(w)
            else:
                return 0

        elif name == '__float__':
            return None

        else:
            print("Could not find attr in Repository: %s"%name)
            return None

    def __unicode__(self):
        return "%s repository: %s (%s)"%(self.type, self.name, self.html_url)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    def link_to_raw_file_in_repo(self, filename):
        return self.check_file_template % (self.full_name, filename)

    def check_file_in_repository(self, filename):

        try:
            url = self.link_to_raw_file_in_repo(filename)
            #print("Checking: %s"%url)
            urlopen(url)
            return True
        except HTTPError:
            return False

    def copy_file_from_repository(self, filename, local_file):

        try:
            url_file = self.link_to_raw_file_in_repo(filename)
            copy_file_from_url(url_file, local_file)
            return True
        except HTTPError:
            return False

    def list_files_in_repo(self):
        rest_url = self.list_files_template%(self.full_name)
        #print("URL: %s"%rest_url)
        try:
            w = get_page(rest_url, utf8=True)
        except:
            return []
        json_files = json.loads(w)
        if not 'tree' in json_files:
            print("Error!")
            print(json_files)
        files = []
        tree = json_files["tree"]
        for entry in tree:
            files.append(entry["path"])
        return files


class GitHubRepository(Repository):

    def __init__(self, info_array):
        Repository.__init__(self, \
                            info_array, \
                            "GitHub", \
                            "https://github.com/%s/raw/master/%s", \
                            "https://api.github.com/repos/%s/git/trees/master?recursive=1")

    @staticmethod
    def create(github_repo_str):

        if github_repo_str is None:
            print("Empty github_repo_str")
            return None

        if github_repo_str.endswith(".git"):
             github_repo_str = github_repo_str[:-4]

        if not github_repo_str.startswith('https://github.com'):
            print("Incorrectly formatted github_repo_str: %s"%github_repo_str)
            return None

        if not len(github_repo_str.split('/')) == 5:
            print("Incorrectly formatted github_repo_str: %s"%github_repo_str)
            return None


        repo = "https://api.github.com/repos/"+github_repo_str[19:]
        page = get_page(repo, utf8=True)
        gh = json.loads(page)
        '''for g in gh:
            print("%s = <<%s>>"%(g, gh[g]))'''
        ghr = GitHubRepository(gh)
        return ghr



if __name__ == "__main__":
    ghr = GitHubRepository.create('https://github.com/NeuroML/NeuroML2')
    ghr = GitHubRepository.create('https://github.com/NeuroML/NeuroML2.git')

    print(ghr)
    print("Repo: %s"%ghr)
    print(ghr.clone_url)

    print(ghr.check_file_in_repository("README"))
    print(ghr.check_file_in_repository("README.md"))

    print("Done")
