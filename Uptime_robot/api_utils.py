from log_utils import *
import requests
import json

PODAPI_SERVER_ADDRESS = str("https://podapi.qikpod.com:8989/")
Log.debug("*** LOADING MODULE = [APIUTILS] ***")

Log.debug("*** LOADING MODULE = [APIUTILS] ***")


def call_rest_api(request_type, endpoint, data=None, params=None, files=None, no_token=False):
    Log.debug("call_rest_api: params")
    Log.debug("\trequestpoddiaginfo_type=[" + str(request_type) + "]")
    Log.debug("\tendpoint=[" + str(endpoint) + "]")
    Log.debug("\tdata=[" + str(data) + "]")
    Log.debug("\tparams=[" + str(params) + "]")
    Log.debug("\tfiles=[" + str(files) + "]")

    REQUESTS_TIMEOUT = 5

    # Added
    STR_API_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZXNzYWdlIjoidG9rZW4gZ2VuZXJhdGVkIGZvciB0ZXN0aW5nIHB1cnBvc2UiLCJleHAiOjE2NzAzOTQyNzR9.chk_l90pZlnDsPu8xP0tV7JRSLAMkb0gzHy487Uce2Q'
    api_access_token = STR_API_ACCESS_TOKEN

    access_token = api_access_token
    headers_dict = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(access_token)}
    # ***

    try:
        url = endpoint
        if request_type == "get":
            if no_token == True:
                api_response = requests.get(url, params=params, verify=False, timeout=REQUESTS_TIMEOUT)
            elif no_token == "status":
                api_response = requests.get(url, params=params, verify=False, timeout=REQUESTS_TIMEOUT).text
                return api_response
            else:
                api_response = requests.get(url, params=params, verify=False, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
        elif request_type == "put":
            api_response = requests.put(url, data=data, verify=False, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
        elif request_type == "post":
            api_response = requests.post(url, data=data, verify=False, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
        elif request_type == "patch":
            api_response = requests.patch(url, data=data, verify=False, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
        elif request_type == "delete":
            api_response = requests.delete(url, params=params, verify=False, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
        elif request_type == "upload_file":
            api_response = requests.post(url, verify=False, files=files, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
        elif request_type == "download_file":
            api_response = requests.get(url, verify=False, params=params, timeout=REQUESTS_TIMEOUT, headers=headers_dict)
            # in this REST call file contents is returned as a byte stream so just return the reponse.
            # no JSON response available in this case
            return api_response
        else:
            print("call_rest_api - ERROR - unknown request_type")
            api_response = ""

        Log.debug("call_rest_api: IN api_response=[" + str(api_response) + "]")
        return_json = api_response.json()
        Log.debug("call_rest_api: OUT return_json=[" + str(return_json) + "]")

    except Exception as e:
        Log.error("call_rest_api: Exception Error occurred error=[" + str(e) + "]")
        return_json = {'success': False}

    return return_json


def call_echoapi():
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'echo/?verbose=true', data=None, params=None)
    if response.has_key('success'):
        breturn = response['success']
        server_time = None
        Log.debug("call_echoapi: breturn=[" + str(breturn) + "] response=[" + str(response) + "]")
    else:
        breturn = response['access_token']
        server_time = response['server_time']
        Log.debug("call_echoapi: breturn=[" + str(breturn) + "] response=[" + str(response) + "]")
    return breturn, server_time


def call_generate_otp(user_phone):
    # request_data = {'user_phone': user_phone}
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'generate_otp?user_phone=' + str(user_phone), data=None, params=None, no_token=True)
    #    Log.debug(str(response))  # for debugging
    breturn = response['success']
    return breturn


def call_validate_otp(user_phone, otp_text):
    # request_data = {'user_phone=': user_phone, '&otp_text': otp_text}
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'validate_otp?user_phone=' + str(user_phone) + '&otp_text=' + str(otp_text) + "&device_type=pod", data=None, params=None, no_token=True)
    if response["success"] is True:
        token = response['access_token']
        bret = True
    else:
        token = ""
        bret = False

    return bret, token


def call_match_otp_to_doorno(pod_id, otptext):
    # https://podapi.qikpod.com:8989/map_otp_to_door?pod_id=1000000&otp_text=123456
    print(pod_id)
    print(otptext)
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'map_otp_to_door?pod_id=' + str(pod_id) + '&otp_text=' + str(otptext), data=None, params=None)
    # response will look like { "success": true, "door_number": 2, "otp_used": false, "record_id": 1 }
    if response["success"] is True:
        # this id will be used when marking otp as used
        if response["door_number"] is -1:
            doorno = -1
        else:
            doorno = response["door_number"]
    elif response["success"] is False:
        if response["door_number"] is -1:
            doorno = -1
        elif response["door_number"] is -2:
            doorno = -2
        elif response["door_number"] is -3:
            doorno = -3
    else:
        doorno = -4
    return doorno


def call_update_door_status(pod_id, door_number, status):
    # https://podapi.qikpod.com:8989/update_door_status?door_number=1&status=OPEN&pod_id=1000000
    print(pod_id)
    print(door_number)
    print(status)
    response = call_rest_api(request_type='patch', endpoint=PODAPI_SERVER_ADDRESS + 'update_door_status?door_number=' + str(door_number) + "&status=" + str(status) + "&pod_id=" + str(pod_id), data=None, params=None)
    # breturn = response['success']
    return response


def call_savelog(log_eventtime="", log_level="INFO", log_type="pod", log_message="None", log_id=""):
    log_entry = {"log_eventtime": log_eventtime, "log_level": log_level,
                 "log_type": log_type, "log_message": log_message, "log_id": log_id}
    request_data = json.dumps(log_entry)
    response = call_rest_api(request_type='post', endpoint=PODAPI_SERVER_ADDRESS + 'logs', data=request_data, params=None)
    Log.debug("call_savelog: request_data=[" + str(request_data) + "] response=[" + str(response) + "]")
    breturn = response['success']
    return breturn


def call_check_onboard_status(pod_id, state="status"):
    res = call_pod_getinfo(pod_id)
    podinfo_dict = res['records']
    status = [pod_dict['status'] for pod_dict in podinfo_dict]
    certified = [pod_dict['pod_state'] for pod_dict in podinfo_dict]
    pod_status = status[0]
    pod_state = certified[0]
    if state != "status":
        if pod_state != "Certified":
            return False
    else:
        if pod_status is "inactive":
            return False
    return True


def call_upload_file(uploadfilename):
    Log.debug("call_upload_file - **** 1")
    if uploadfilename is None:
        Log.debug("call_upload_file - *** 1.1")
        return False
    if call_path_isfile(uploadfilename) is False:
        Log.debug("call_upload_file - *** 1.2")
        return False

    Log.debug("call_upload_file - **** 2")

    # Now we will upload the log file to the cloud repo
    files_dict = {'in_file': open(uploadfilename, 'rb')}

    Log.debug("call_upload_file - **** 3")
    response = call_rest_api(request_type='upload_file', endpoint=PODAPI_SERVER_ADDRESS + 'filestore/', data=None, params=None, files=files_dict)
    Log.debug('*** call_upload_file response: [%s]' % str(response))
    Log.debug("call_upload_file - **** 4")
    # return True
    if not response['success']:
        # if file does not exits
        return False

    # response = call_api('get', 'download_file', params=params)
    # local_file_name = 'renamed_2022_02_23_13_13_36_pod.log'
    # with open(local_file_name, 'wb') as file:
    #     for chunk in response.iter_content(chunk_size=1024):
    #         file.write(chunk)
    return True


def call_pod_getinfo(pod_id):
    # https://podapi.qikpod.com:8989/pods/1000000
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'pods/' + str(pod_id), data=None, params=None)
    return response


def call_activate_pod(pod_id, verbose=False):
    # https://podapi.qikpod.com:8989/pods/activate/1000005?verbose=true
    if verbose:
        response = call_rest_api(request_type='patch', endpoint=PODAPI_SERVER_ADDRESS + 'pods/activate/' + str(pod_id) + '?verbose=true', data=None, params=None)
    else:
        response = call_rest_api(request_type='patch', endpoint=PODAPI_SERVER_ADDRESS + 'pods/activate/' + str(pod_id) + '?verbose=false', data=None, params=None)
    breturn = response['success']
    return breturn


def call_pod_updateinfo(pod_id, pod_dict, verbose=False):
    # https://podapi.qikpod.com:8989/pods/1000000?verbose=true
    if verbose:
        response = call_rest_api(request_type='patch', endpoint=PODAPI_SERVER_ADDRESS + 'pods/' + str(pod_id) + '?verbose=true', data=json.dumps(pod_dict), params=None)
    else:
        response = call_rest_api(request_type='patch', endpoint=PODAPI_SERVER_ADDRESS + 'pods/' + str(pod_id) + '?verbose=false', data=json.dumps(pod_dict), params=None)
    return response


def call_download_file(download_file_name, local_file_name):
    ireturn = 0
    Log.debug("call_download_file: download_file_name=[" + str(download_file_name) + "] local_file_name=[" + str(local_file_name) + "]")

    if (download_file_name is None) or (local_file_name is None):
        Log.error("call_download_file: bad download or local filename download_file_name=[" + str(download_file_name) + "] local_file_name=[" + str(local_file_name) + "]")
        return RET_BADFILENAME

    # params = {'file_name': download_file_name}
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'filestore/info/?filename=' + download_file_name, data=None, params=None, files=None)
    if response['success'] is not True:
        Log.error('call_download_file: File does not exist')
        return RET_MISSINGCLOUDFILE

    if call_path_isfile(local_file_name) is True:
        Log.error("call_download_file: local file already exists - cannot download local_file_name=[" + str(local_file_name) + "]")
        return RET_LOCALFILEEXISTS

    response = call_rest_api(request_type='download_file', endpoint=PODAPI_SERVER_ADDRESS + 'filestore/' + download_file_name, data=None, params=None, files=None)

    with open(local_file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    # alternate code: open(local_file_name, 'wb').write(response.content)

    Log.debug("call_download_file: successfully download_file_name=[" + str(download_file_name) + "]")
    return 0


def call_download_url_to_file(download_file_url, local_file_name):
    response = requests.get(download_file_url, allow_redirects=True)
    if response:  # evaluate to True if the status code was between 200 and 400
        Log.debug("call_download_url_to_file: FOUND download_file_url=[" + download_file_url + "]")
        open(local_file_name, 'wb').write(response.content)
        return True
    Log.debug("call_download_url_to_file: NOT FOUND download_file_url=[" + download_file_url + "]")
    return False


# *** USE Log calls carefully in this one function since we are archiving the file
def call_backup_logs():
    call_backup_logfile(slogname=ROOT_LOG_FILE, sdir=ROOT_LOG_DIR)
    call_backup_logfile(slogname=ROOT_APPLOG_FILE, sdir=ROOT_LOG_DIR)
    return


# *** USE Log calls carefully in this one function since we are archiving the file
def call_backup_logfile(slogname=ROOT_LOG_FILE, sdir=ROOT_LOG_DIR):
    Log.debug("call_backup_logs: IN slogname=[" + str(slogname) + "] sdir=[" + str(sdir) + "]")
    exitcode = EXIT_OK

    try:
        now = datetime.now()

        datetime_text = str(now.strftime("%Y_%m_%d_%H_%M_%S"))
        Log.debug("call_backup_logs: datetime_text=[" + str(datetime_text) + "]")

        src = call_path_join(str(sdir), str(str(slogname)))
        dst = call_path_join(str(sdir), str(str(datetime_text) + str("_") + str(slogname)))

        Log.debug("call_backup_logs: src=[" + str(src) + "] => dst=[" + str(dst) + "]")

        Log.debug("call_backup_logs: rename current log file to archive it")
        if call_path_isfile(src) is True:
            Log.debug("call_backup_logs: RENAMING LOG FILE from src=[" + str(src) + "] => dst=[" + str(dst) + "]")
            call_path_rename(src, dst)
            call_upload_file(dst)
        else:
            Log.debug("call_backup_logs: MISSING LOG FILE src=[" + str(src) + "] so did not archive it")

    except Exception as error_msg:
        Log.debug("call_backup_logs: failed error_msg=[" + str(error_msg) + "]")
        exitcode = EXIT_FAILURE
        pass

    Log.debug("call_backup_logs: OUT")
    return exitcode
