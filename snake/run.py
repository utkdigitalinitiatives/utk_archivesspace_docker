import requests
import json
import time
import sys
from requests.exceptions import ConnectionError
import os
from pathlib import Path
from data import accessions


class ArchiveSpace:
    def __init__(self,
                 url: str = 'http://utkarchivesspacedocker_archivesspace_1',
                 user: str = 'admin',
                 password: str = 'admin'):
        self.base_url = url
        self.username = user
        self.password = password
        self.headers = {}
        self.__test_if_service_up()
        self.session = self.__authenticate()
        self.headers = {'X-ArchivesSpace-Session': self.session}
        self.records = self.add_sample_resources('data/eads')
        self.__test_if_data_exists()

    def __authenticate(self):
        r = requests.post(url=f'{self.base_url}:8089/users/{self.username}/login?password={self.password}')
        print(r.json)
        return r.json()['session']

    def __test_if_service_up(self):
        try:
            r = requests.get(url=f'{self.base_url}:8080')
            if r.status_code != 200:
                print(r.status_code)
                print(f'ArchivesSpace is showing {r.status_code}. Waiting 15 seconds to retry service.')
                time.sleep(15)
                return self.__test_if_service_up()
            else:
                return
        except ConnectionError as e:
            print(e)
            time.sleep(30)
            return self.__test_if_service_up()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return self.__test_if_service_up()

    def __test_if_repositories_were_created(self):
        r = requests.get(url=f'{self.base_url}:8089/repositories', headers=self.headers)
        if len(r.json()) >= 1:
            print(f"ArchivesSpace has {len(r.json())} repositories.")
            return
        else:
            print(f'ArchivesSpace is still building.  Waiting 15 seconds and recreating.')
            return self.create_repository()

    def __test_if_data_exists(self):
        #self.delete_repository()
        r = requests.get(url=f'{self.base_url}:8089/repositories', headers=self.headers)
        print(r.content)
        if len(r.json()) >= 1:
            print(f"ArchivesSpace has data:")
            for repo in r.json():
                print(repo)
            return
        else:
            print("ArchivesSpace has no data.  Building repositories.")
            self.create_repository()
            return

    def create_repository(self):
        r = requests.post(url=f'{self.base_url}:8089/repositories',
                          headers=self.headers,
                          data=json.dumps(
                              {
                                  "lock_version": 0,
                                  "repo_code": "UTK",
                                  "name": "Betsey B. Creekmore Special Collections and University Archives",
                                  "created_by": "admin",
                                  "last_modified_by": "admin",
                                  "create_time": "2018-11-26T20:18:07Z",
                                  "system_mtime": "2018-11-26T20:18:07Z",
                                  "user_mtime": "2018-11-26T20:18:07Z",
                                  "publish": True,
                                  "oai_is_disabled": False,
                                  "jsonmodel_type": "repository",
                                  "uri": "/repositories/2",
                                  "display_string": "Betsey B. Creekmore Special Collections and University Archives",
                                  "agent_representation": {
                                      "ref": "/agents/corporate_entities/1"
                                  }
                              }
                          ),
                          )
        self.__test_if_repositories_were_created()
        if r.status_code == 400:
            print("Sleeping 10 seconds.")
            time.sleep(10)
            self.create_repository()
        self.create_import_jobs()
        return self.__add_sample_accessions()

    @staticmethod
    def add_sample_resources(path):
        for record in os.walk(path):
            return [file for file in record[2] if file.endswith(".xml")]

    def delete_repository(self):
        r = requests.delete(url=f'{self.base_url}:8089/repositories/2',
                            headers=self.headers)
        return

    def create_records(self):
        for file in self.records:
            with open(f'data/eads/{file}', 'r') as record:
                text = record.read()
                r = requests.post(url=f'{self.base_url}:8089/repositories/2/resources',
                                  headers=self.headers,
                                  data=text)
                print(f'{r.status_code} for {file}.  \n {r.json()}')
        return

    def create_import_jobs(self):
        print(f'Creating jobs to add {self.records}')
        for file in self.records:
            current_file = os.path.abspath(f'data/eads/{file}')
            filename = [Path(current_file).stem]
            test = [("files[]", open(current_file, "rb"))]
            print(current_file)
            job = json.dumps({
                "job_type": "import_job",
                "job": {
                    "import_type": "ead_xml",
                    "jsonmodel_type": "import_job",
                    "filenames": filename
                }
            })
            r = requests.post(url=f'{self.base_url}:8089/repositories/2/jobs_with_files',
                              headers=self.headers,
                              params={"job": job},
                              files=test
                              )
            print(f'{r.status_code} for {file}. \n\t {r.json()}')
        return

    def __add_sample_accessions(self):
        for accession in accessions.accessions:
            r = requests.post(url=f'{self.base_url}:8089/repositories/2/accessions',
                              headers=self.headers,
                              data=json.dumps(accession)
                              )
            print(f'{r.status_code}: {r.json()}')
        return


if __name__ == "__main__":
    print("Starting ArchivesSpace connection.")
    x = ArchiveSpace()
