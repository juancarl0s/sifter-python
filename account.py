import requests
import json
import project


class Account(object):
    """Account wrapper for Sifter"""
    def __init__(self, host, token, include_archived):
        self.host = host
        self.token = token
        self.include_archived = include_archived
        self.url = 'https://' + self.host + '.sifterapp.com' + '/api/projects?all=' + str(include_archived)

    def request(self, url):
        """Requests JSON object from Sifter URL"""
        req = requests.get(url, headers={'X-Sifter-Token': self.token,
                                         'Accept': 'application/json'})

        try:
            loadcontent =  json.loads(req.content)
        except ValueError:
            return loadcontent['issue']
        else:
            return loadcontent

    def projects(self):
        """Gets all the projects from sifter"""
        projects = []
        json_raw = self.request(self.url)
        raw_projects = json_raw['projects']
        for raw_project in raw_projects:
            proj = project.Project(raw_project, self)
            projects.append(proj)

        return projects
