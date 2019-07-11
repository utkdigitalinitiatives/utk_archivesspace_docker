import requests
import json


class ArchiveSpace:
    def __init__(self, url: str = 'http://172.18.0.1:8089/', user: str = 'admin', password: str = 'admin'):
        self.base_url = url
        self.username = user
        self.password = password
        self.headers = {}
        self.session = self.__authenticate()
        self.headers = {'X-ArchivesSpace-Session': self.session}

    def __authenticate(self):
        r = requests.post(url=f'{self.base_url}users/{self.username}/login?password={self.password}')
        return r.json()['session']

    def create_repository(self):
        r = requests.post(url=f'{self.base_url}/repositories',
                          headers=self.headers,
                          data=json.dumps(
                              {
                                  "lock_version": 0,
                                  "repo_code": "UTK",
                                  "name": "University of Tennessee Libraries, Special Collections",
                                  "created_by": "admin",
                                  "last_modified_by": "admin",
                                  "create_time": "2018-11-26T20:18:07Z",
                                  "system_mtime": "2018-11-26T20:18:07Z",
                                  "user_mtime": "2018-11-26T20:18:07Z",
                                  "publish": True,
                                  "oai_is_disabled": False,
                                  "jsonmodel_type": "repository",
                                  "uri": "/repositories/2",
                                  "display_string": "University of Tennessee Libraries, Special Collections (UT)",
                                  "agent_representation": {
                                      "ref": "/agents/corporate_entities/1"
                                  }
                              }
                          )
                          )
        return


if __name__ == "__main__":
    x = ArchiveSpace()
    x.create_repository()

