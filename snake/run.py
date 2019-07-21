import requests
import json
import time


class ArchiveSpace:
    def __init__(self, url: str = 'http://172.18.0.1', user: str = 'admin', password: str = 'admin'):
        self.base_url = url
        self.username = user
        self.password = password
        self.headers = {}
        self.__test_if_service_up()
        self.session = self.__authenticate()
        self.headers = {'X-ArchivesSpace-Session': self.session}

    def __authenticate(self):
        r = requests.post(url=f'{self.base_url}:8089/users/{self.username}/login?password={self.password}')
        return r.json()['session']

    def __test_if_service_up(self):
        r = requests.get(url=f'{self.base_url}:8080')
        if r.status_code != 200:
            print(f'ArchivesSpace is showing {r.status_code}. Waiting 15 seconds to retry service.')
            time.sleep(15)
            return self.__test_if_service_up()
        else:
            print(r.content)
            return

    def create_repository(self):
        r = requests.post(url=f'{self.base_url}:8089/repositories',
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
        print(r.status_code)
        if r.status_code == 400:
            print("Sleeping 10 seconds.")
            time.sleep(10)
            self.create_repository()
        return


if __name__ == "__main__":
    x = ArchiveSpace()
    x.create_repository()

