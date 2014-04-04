
from __init__ import *

import json

class Repository():
    
    type = "???"
    
    NAME = 'name'
    URL = 'url'
    HTML_URL = 'html_url'
    HAS_WIKI = 'has_wiki'
    OPEN_ISSUES = 'open_issues'
    FORKS = 'forks'
    WATCHERS = 'watchers'
    
    def __init__(self, info_array, type):
        self.type = type
        self.info_array = info_array
        
        
    def __getattr__(self, name):
        
        if name == self.NAME:
            return self.info_array[self.NAME]
        
        if name == self.URL:
            return self.info_array[self.URL]
        
        if name == self.HTML_URL:
            return self.info_array[self.HTML_URL]
        
        if name == self.OPEN_ISSUES:
            oi = self.info_array[self.OPEN_ISSUES]
            if oi is not None:
                return int(oi)
            else:
                return 0
        if name == self.HAS_WIKI:
            return self.info_array[self.HAS_WIKI]
        
        if name == self.FORKS:
            f = self.info_array[self.FORKS]
            if f is not None:
                return int(f)
            else:
                return 0
            
        if name == self.WATCHERS:
            w = self.info_array[self.WATCHERS]
            if w is not None:
                return int(w)
            else:
                return 0
        else:
            return None
        
    def __str__(self):
        return "%s repository: %s (%s)"%(self.type, self.name, self.html_url)
        
        
class GitHubRepository(Repository):
    
    def __init__(self, info_array):
        Repository.__init__(self, info_array, "GitHub")
        
    @staticmethod
    def create(github_repo_str):
        
        if github_repo_str.endswith(".git"):
             github_repo_str = github_repo_str[:-4]

        repo = "https://api.github.com/repos/"+github_repo_str[19:]
        page = get_page(repo)
        gh = json.loads(page)
        ghr = GitHubRepository(gh)
        return ghr
        
        
        
        
if __name__ == "__main__":

        
    ghr = GitHubRepository.create('https://github.com/OpenSourceBrain/GranCellLayer')
    
    print ghr
    
    print("Done")
