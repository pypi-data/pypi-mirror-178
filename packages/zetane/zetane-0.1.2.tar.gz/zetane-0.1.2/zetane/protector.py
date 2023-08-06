import os, filetype, time, json, sys
from xmlrpc.client import Boolean
from tqdm import tqdm
import requests as req
from zipfile import ZipFile

ADDRESS = "https://protector-api-1.zetane.com/"
# ADDRESS = "http://localhost:8000/"


def api_url_builder(client, datatype=""):
    return ADDRESS + 'api/' + client.org + '/' + client.project + '/' + datatype

def req_handle(url, client, method, body=None, json_bool=False):
    #print('CLIENT: ', client.keys())
    headers = {"Authorization": "Token " + client.api_key}
    if method == "get":
        res = req.get(url, headers=headers)
    if method == "post":
        if json_bool:
            res = req.post(url, json=body, headers=headers)
        else:
            res = req.post(url, data=body, headers=headers)
    if method == "put":
        if json_bool:
            res = req.put(url, json=body, headers=headers)
        else:
            res = req.put(url, data=body, headers=headers)


    if res.status_code != 200 and res.status_code != 201 and res.status_code != 202:
        print('STATUS CODE: ', res.status_code)
        raise NetworkError(res)
    return res

def check_org_in_user(self, org):
    user = self.user
    for org_temp in user['organizations']:
        if org_temp['name'] == org:
            return True
    print('Organization name is invalid')
    return False

def check_project_in_org(self, org, project_to_check):
    user = self.user
    org_check = None
    for org_tmp in user['organizations']:
        if org_tmp['name'] == org:
            org_check = org_tmp
    for project in org_check['projects']:
            if project['name'] == project_to_check:
                return True
    print('Project name is invalid')
    return False

def file_helper(file_path, metadata):
    filename = os.path.basename(file_path)
    absolute_file_path = os.path.abspath(file_path)
    file_size = os.path.getsize(absolute_file_path)
    file_type = filetype.guess_mime(absolute_file_path)
    body = {"filename": filename, "file_type": file_type, "file_size": file_size, "source": "API", "metadata": json.dumps(metadata)}
    newObj = {
            'upload_status': { 'status': "Pending" },
            'dataset_type': 'classification',
        }

    body = {**body, **newObj}
    return body


class NetworkError(Exception):
    def __init__(self, result, message=""):
        self.result = result
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.result.reason + ' ' + str(self.result.status_code) + ' at ' + self.result.url + ' -> ' + self.result.text

class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class Protector(Borg):
    def __init__(self, api_key=None, org=None, project=None):
        Borg.__init__(self)
        self.config(api_key=api_key, org=org, project=project)

    def auth_check(self):
        if not hasattr(self, 'api_key') or not self.api_key:
            raise SystemExit('Failed to authenticate API key')

    def config(self, project=None, org=None, api_key=None):
        if api_key:
            self.api_key = api_key
            try:
                res = req_handle(ADDRESS + "users/me", self, 'get')
                user = res.json()
                print('SUCCESSFULLY AUTHENTICATED USER')
                self.user = user
            except:
                self.api_key = None
                self.org = None
                self.project = None
                self.model = None
                self.report = None
                self.dataset = None
                self.user = None
                return print('''API KEY is invalid. You can retrieve your api key from:
                protector.zetane.com''')
        if org and check_org_in_user(self, org):
            self.org = org
            print('Organization configuration successful')
        if self.org and project and check_project_in_org(self, self.org, project):
            self.project = project
            print('Project configuration successful')

    def test(self):
        return self.api_key

    def test_large(self):
        return f'APIKEY: {self.api_key}, PROJECT: {self.project}, ORG: {self.org}'

    def get_orgs_and_projects(self):
        self.auth_check()
        res = req_handle(ADDRESS + 'users/me', self, 'get')
        user = res.json()
        for org in user['organizations']:
            print(org['name'])
            for project in org['projects']:
                print('\t' + project['name'])

    def link_org(self, project):
        res = req_handle(ADDRESS + "users/me")
        user = res.json()
        try:
            for org in user.organizations:
                for project_key in org.projects:
                    if project_key.name == project:
                        self.project = f"{org.name}/{project_key.name}"
        except:
            print("Error retrieving organizations!")

        if self.project is None:
            print("Project not found! Searched the following projects: ")
            print(f"{user.organizations}")

    def upload_dataset(self, file_path='', org=None, project=None):
        self.auth_check()
        print('Starting dataset upload..')
        self.config(project=project, org=org)
        # metadata = construct_metadata_obj(file_path)
        # if not metadata:
        #     print('Please select a zipped file to upload')
        #     return
        # return
        body = file_helper(file_path, {})
        post_url = api_url_builder(self, "dataset")
        res = req_handle(post_url, self, "post", body)

        dataset_id = res.json()["id"]
        dataset_name = res.json()['name']
        res = upload(self, "datasets", dataset_id, file_path)
        res = confirm_upload(self, "datasets", dataset_id, file_path)
        self.dataset = dataset_name
        print("Completed")
        return res

    def upload_model(self, file_path, org=None, project=None):
        self.auth_check()
        print('Starting model upload...')
        self.config(project=project, org=org)
        # metadata = construct_metadata_obj(file_path)
        # if not metadata:
        #     print('Please select a zipped file to upload')
        #     return
        body = file_helper(file_path, {})
        post_url = api_url_builder(self, "model")
        res = req_handle(post_url, self, "post", body)
        model_id = res.json()["id"]
        model_name = res.json()['name']
        res = upload(self, "models", model_id, file_path)
        res = confirm_upload(self, "models", model_id, file_path)
        res = build_image(self, model_id)
        self.model = model_name
        print('MODEL NAME: ', self.model)
        print("Completed")
        return res

    def get_entries(self, datatype, org=None, project=None):
        self.auth_check()
        print("Getting entries..")
        if datatype != 'models' and datatype != 'datasets':
            return print('Only available datatypes are "models" or "datasets"')
        self.config(project=project, org=org)
        if not self.project:
            return print('Please select a project')
        url = api_url_builder(self, datatype)
        res = req_handle(url, self, "get")

        if res.status_code == 200:
            for x in res.json():
                if not x['name']:
                    continue
                print(f'ID: {str(x["id"])} NAME: {x["name"]}')

    def get_report_status(self, name, org=None, project=None):
        self.auth_check()
        self.config(project=project, org=org)
        token = self.api_key
        headers = {"Authorization": "Token " + token}
        url = api_url_builder(self) + f"/{name}/status"
        res = req_handle(url, self, "get")
        curr_status = res.json()["status"]
        if curr_status != "Running" and curr_status != "Pending":
            if res.status_code == 200:
                res = req.get(url + "/" + name + "/report", headers=headers)
            else:
                raise NetworkError(res, "Failed Execution")
        else:
            print('Report Name: ' + name)
            print('Report Status: ' + curr_status)

    def report(self, test_profile_path, organization=None, project=None, model=None, dataset=None, autoRun=False):
        self.auth_check()
        if not hasattr(self, 'api_key'):
            return print('Report creation failed - please configure the Protector API to use you API key')
        if not model and not hasattr(self, 'model'):
            return print('Report creation failed - please specify which model you wish to use')
        if not dataset and not hasattr(self, 'dataset'):
            return print('Report creation failed - please specify which dataset you wish to use')
        if not organization and not hasattr(self, 'org'):
            return print('Report creation failed - please specify which organization you wish to use')
        if not project and not hasattr(self, 'project'):
            return print('Report creation failed - please specify which project you wish to use')
        token = self.api_key
        model = model if model else self.model
        dataset = dataset if dataset else self.dataset
        organization = organization if organization else self.org
        project = project if project else self.project


        # try:
        #     model = model if model else self.model
        #     dataset = dataset if dataset else self.dataset
        #     organization = organization if organization else self.org
        #     project = project if project else self.project

        # except:
        #     print('Failed to create report:')
        #     return print('Please ensure that you have configured your organization and project and specified both the desired model and dataset files in your report creation call')
        self.config(org=organization, project=project)
        headers = {"Authorization": "Token " + token}
        if not validate_file_type(test_profile_path):
            print('Please attach a JSON test file.')
            return

        #get model ID
        try:
            URL = ADDRESS + "/api/" + organization + "/" + project + '/' + 'models'
            res = req.get(URL, headers=headers)
            #UPDATE THESE CALLS
            if not res.status_code == 200:
                print('Invalid model selection')
            models_json = res.json()
            models_match = [v['id'] for v in models_json if v['name'] == model]
            model_id = max(models_match)
        except:
            print('Invalid model selection - please select from the following or upload a new model:')
            return self.get_entries('models')

        #get dataset ID
        try:
            URL = ADDRESS + "/api/" + organization + "/" + project + '/' + 'datasets'
            res = req.get(URL, headers=headers)
            if not res.status_code == 200:
                print('Invalid dataset selection')
            dataset_json = res.json()
            datasets_match = [v['id'] for v in dataset_json if v['name'] == dataset]
            dataset_id = max(datasets_match)
        except:
            print("Invalid dataset selection - please select from the following or upload a new model:")
            return self.get_entries('datasets')


        test_series_name = test_profile_path.split('/')[-1]
        crafted_test_profile = validate_file(test_profile_path, model, model_id, dataset, dataset_id, test_series_name)

        url = api_url_builder(self, "run")
        body = {"save": False, "data": crafted_test_profile, "supValues": { "numPrimaryTests": '', "numComposedTests": '', "totalTestRuns": '', "totalXaiApplied": '' }}
        res = req_handle(url, self, "post", body, json_bool=True)
        name = None
        name = res.json()["name"]

        if res.status_code == 201:
            print("Starting report: " + name)
            print('When completed, your report can be found at the following url:')
            print('protector.zetane.com' + '/' + self.org + '/' + self.project + '/' + 'runs/' + name)
            if (autoRun):
                i = 0
                while True:
                    time.sleep(10)
                    i += 1
                    res = req.get(URL + "/" + name + "/status", headers=headers)
                    if res.status_code == 200:
                        print("Running... " + str(10 * i) + " seconds")
                        if res.json()["status"] != "Running" and res.json()['status'] != "Pending":
                            break
                    else:
                        break
                if res.status_code == 200:
                    res = req.get(URL + "/" + name + "/report", headers=headers)
                else:
                    raise NetworkError(res, "Failed Execution")
        else:
            raise NetworkError(res, "Failed Execution")

        # if res.status_code != 200:
        #     raise NetworkError(res, "Failed Report")
        # print("Completed")
        return res


############################## END OF CLASS ######################################
# def handleErr(errCode, jobType, res):
#     if jobType == 'report' and (errCode != 200 or errCode != 201):
#         raise NetworkError(res, "Failed Report")

#     return

def confirm_upload(client, datatype, id, file_path):
    filename = os.path.basename(file_path)
    body = {"name": filename, "upload_status": {"status": "Ready"}}
    url = api_url_builder(client, datatype) + f"/{str(id)}"
    return req_handle(url, client, "put", body, json_bool=True)


def upload(client, datatype, id, file_path):
    FILE_CHUNK_SIZE = 10000000  # 10MB
    absolute_file_path = os.path.abspath(file_path)
    file_size = os.path.getsize(absolute_file_path)
    NUM_CHUNKS = (file_size - 1) // FILE_CHUNK_SIZE + 1
    file_type = filetype.guess_mime(absolute_file_path)

    url = api_url_builder(client, datatype) + f"/{str(id)}"
    res = req_handle(url + '/upload', client, "post", {"fileType": file_type})
    # Initialize multi-part
    upload_id = res.json()["uploadId"]

    # Upload multi-part
    parts = []
    with open(absolute_file_path, "rb") as file:
        for index in tqdm(range(NUM_CHUNKS)):
            offset = index * FILE_CHUNK_SIZE
            file.seek(offset, 0)

            res = req_handle(url + "/upload_part",
                            client,
                            "post",
                           {"part": index + 1, "uploadId": upload_id})
            presigned_url = res.json()["presignedUrl"]
            res = req.put(presigned_url, data=file.read(FILE_CHUNK_SIZE), headers={"Content-Type": file_type})
            parts.append({"ETag": res.headers["etag"][1:-1], "PartNumber": index + 1})

    # Finalize multi-part
    res = req_handle(url + "/upload_complete", client, "post", {"parts": parts, "uploadId": upload_id}, json_bool=True)
    return res


def build_image(client, id):
    url = api_url_builder(client, "models") + f"/{str(id)}/image"
    res = req_handle(url, client, "post", {id: id})
    if res.status_code == 201:
        name = res.json()["name"]
        i = 0
        while True:
            time.sleep(10)
            i += 1
            url = api_url_builder(client) + f"{name}/image/status"
            res = req_handle(url, client, "get")
            if res.status_code == 200:
                print("Building... " + str(10 * i) + " seconds")
                status = res.json()["status"]["status"]
                if status != "Running" and status != "Pending":
                    break
            else:
                print('Not building image...')
                break
    return res

def recurz(arrOfPaths, dict):
    if len(arrOfPaths) > 1:
        if arrOfPaths[0] not in dict:
            dict[arrOfPaths[0]] = {'type': '', 'size': ''}
        recurz(arrOfPaths[1:], dict[arrOfPaths[0]])
    else:
        dict[arrOfPaths[0]]= {'type': arrOfPaths[0].split('.')[-1] if '.' in arrOfPaths[0] else '', 'size': ''}
    return

def construct_metadata_obj(file_path):
    absolute_file_path = os.path.abspath(file_path)
    if not absolute_file_path.endswith('.zip'):
        return False
    metadata = {}
    with ZipFile(absolute_file_path, 'r') as zipObj:
        listOfilesFirst = zipObj.namelist()
        listOfFiles = [x for x in listOfilesFirst if 'macosx' not in x.lower()]
        for fileName in listOfFiles:
            arrOfPaths = fileName.split('/')
            recurz(arrOfPaths, metadata)

        return metadata


def validate_file_type(file_path):
    absolute_file_path = os.path.abspath(file_path)

    file_size = os.path.getsize(absolute_file_path)
    file_type = filetype.guess_mime(absolute_file_path)
    # print(file_type, file_size, absolute_file_path)
    if file_type != 'application/json' and not '.json' in file_path:
        return False
    return True

def check_if_valid_test(test, max, min, intervals):
    test = test.replace(' ', '_')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    absolute_file_path = os.path.abspath(dname+'/user_transformation_table.json')

    with open(absolute_file_path, 'r', encoding='utf-8') as reference_file:

        reference_obj = json.loads(reference_file.read())
        if not max or not min or not intervals:
            return False

        if test not in reference_obj:
            return False
        max_lim = reference_obj[test]['range_max']
        min_lim = reference_obj[test]['range_min']

        if max_lim < max or max_lim < min:
            return False
        if min_lim > min or min_lim > max:
            return False

    return True

def validate_file(file_path, model, model_id, dataset, dataset_id, test_series='dev'):
    f = open(file_path)
    tests = json.load(f)
    testArr = [] #array of test objects
    xaiObj = {}
    for test in tests:
        #first check if the test is a real test & if the ranges and intervals are within acceptable limits
        if not check_if_valid_test(test, tests[test]['max'], tests[test]['min'], tests[test]['intervals']):
            print(f'{test} was invalid and was not included.')
            continue
        #if both of above are good, then construct object
        if 'xai' in tests[test]:
            #add to xai obj
            xaiObj = xaiObj.get(test, []) + tests[test]['xai']

        test_obj = {
            "name": test,
            "number_of_tests": tests[test]['intervals'],
            "sequence": {
                "function": test,
                "min_range": tests[test]['min'],
                "max_range": tests[test]['max']
            }
        }
        testArr.append(test_obj)
    f.close()

    test = {
        "info": {
            "specs_version": 0.1,
            "source": 'api',
            "report_id": 'dev_test1'
        },
        "model": {
            "model_id": model_id,
            "mlflow_model_folder_path": '',
            "filename": model
        },
        "dataset": {
            "dataset_id": dataset_id,
            "dataset_folder_path": '',
            "labels_file_path": '',
            "class_list": '',
            "class_list_path": '',
            "filename": dataset
        },
        "ground_truth": {
            "annotations_path": '',
        },
        "model_type": 'image_classification',
        "sample_size": {
            "number": 0,
            "percentage": 100
        },
        "framework": 'image_classification',
        "xai": xaiObj,
        "robustness": {
            "test_series": test_series,
            "tests": testArr
        }
    }
    return test
