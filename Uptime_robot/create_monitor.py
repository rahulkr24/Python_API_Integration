import re

from api_utils import *
import requests
import time
import csv
from datetime import datetime, timedelta

POD1 = "u1888140-d78498a229dc7d28d336bba6"
POD2 = "u1888143-ef8b448b33a1046d9f5349d1"
POD3 = "u1889112-324fdd3fc60eec0d78bc7606"
POD4 = "u1904758-7d33983157980c4adb55dff5"
POD5 = "u1888386-f0197b3dc44c5f7de9d278c6"  # rahulkumar.rj24@gmail.com ---Rahul@123
api_key = [POD2, POD3, POD4]
Friendly_Name = []
M_Friendly_Name = []
url = []
M_url = []
m_id_list = []
ids = []
down_id = []
down_pod = {}
list1 = []
get_url = []
get_name = []
id_list = []
pod_dict = {}
data = []
non_match_url = []
non_match_name = []
duplicate_list = []
non_match_id = []

now = int(round(time.time() * 1000) + 19800000)
print(now)
hours_6 = now - 2.16e+7
print(hours_6)


def get_pod_details():
    response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'pods/')
    print("*********************************************************************************")
    for item in response["records"]:
        # print(item["pod_name"])
        if "Qik" not in item["location_name"] and 'pod_name' not in item["pod_name"] and item["status"] != 'inactive' and item["pod_state"] == 'Certified':
            # print(item)
            id = item["id"]
            new_pod_id = "POD_" + str(item["id"]) + "_" + item["pod_name"]
            Friendly_Name.append(new_pod_id)
            new_url = "https://appapi.qikpod.com:8989/status/" + str(item["id"])
            url.append(new_url)
            id_list.append(id)
    print(len(id_list))
    print(Friendly_Name)
    print(url)


def pod_status():
    for i in id_list:
        response = call_rest_api(request_type='get', endpoint=PODAPI_SERVER_ADDRESS + 'status/' + str(i), no_token="status")
        txt = re.search(r'<h1>(.*?)</h1>', response).group(1)
        print(i, ":", txt)


def find_new_pod_monitor():
    for i in api_key:
        url2 = "https://api.uptimerobot.com/v2/getMonitors"
        payload = "api_key=" + i + "&format=json&logs=1"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url2, data=payload, headers=headers)
        txt = response.json()
        for item in txt['monitors']:
            name = item["friendly_name"]
            url_ = item["url"]
            get_name.append(name)
            get_url.append(url_)
            if name not in Friendly_Name:
                non_match_id.append(item["id"])
    print(len(get_name))
    print(non_match_id)
    for k in Friendly_Name:
        if k not in get_name:
            non_match_name.append(k)
    for k in url:
        if k not in get_url:
            non_match_url.append(k)
    print(non_match_name)
    print(non_match_url)


def add_new_find_monitor():
    count = 0
    for i in range(len(non_match_url)):
        url_ = "https://api.uptimerobot.com/v2/newMonitor"
        payload2 = "api_key=" + POD4 + "&format=json&type=2&url=" + str(non_match_url[i]) + "&friendly_name=" + str(non_match_name[
                                                                                                                        i]) + "&keyword_type=2&keyword_value=Device Up&keyword_case_type=1&alertcontact>type=qa4@qikpod.com"
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url_, data=payload2, headers=headers)
        txt = response.json()
        print(txt)
        time.sleep(10)
        if txt["stat"] == "fail":
            print("Failed to create Monitor")
            print(txt)
            print("https://uptimerobot.com/dashboard#mainDashboard")
            count += 1
            print("Add Monitor Count :", count)
            time.sleep(5)
    print("Go to Uptime and Check its Created : https://uptimerobot.com/dashboard#mainDashboard")


def add_monitor(start, end, key):
    count = 0
    for i in range(start, end, 1):
        url_ = "https://api.uptimerobot.com/v2/newMonitor"
        payload2 = "api_key=" + key + "&format=json&type=2&url=" + str(url[i]) + "&friendly_name=" + str(Friendly_Name[i]) + "&keyword_type=2&keyword_value=Device Up&keyword_case_type=1&alertcontact>type=qa4@qikpod.com"
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url_, data=payload2, headers=headers)
        txt = response.json()
        print(txt)
        count += 1
        time.sleep(7)
        if txt["stat"] == "fail":
            print("Failed to create Monitor")
            print(response.json())
            print("https://uptimerobot.com/dashboard#mainDashboard")
        print("Add Monitor Count :", count)
        time.sleep(6)
    print("Go to Uptime and Check its Created : https://uptimerobot.com/dashboard#mainDashboard")


def down_pod_monitor():
    for i in api_key:
        url2 = "https://api.uptimerobot.com/v2/getMonitors"
        payload = "api_key=" + i + "&format=json&logs=1&all_time_uptime_ratio=1&response_times_start_date=" + str(hours_6)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url2, data=payload, headers=headers)
        txt = response.json()
        get_pod = csv.writer(open("Down_Monitor.csv", 'a'))
        get_pod.writerow(txt["monitors"][0])
        for line in txt['monitors']:
            data = line["logs"]
            for i in data:
                j = i["reason"]
                if (j["code"]) == "888888":
                    print("Device Down")
                    pod_name = line["friendly_name"]
                    pod_url = line["url"]
                    id_ = line["id"]
                    down_id.append(id_)
                    M_Friendly_Name.append(pod_name)
                    M_url.append(pod_url)
                    print(line["friendly_name"], line["url"])
                    down_m = line.values()
                    get_pod.writerow(down_m)
            time.sleep(2)
    print(len(M_url))


def get_all_monitor():
    f = open("GetMonitor.csv", "w")
    f.truncate()
    for i in api_key:
        url2 = "https://api.uptimerobot.com/v2/getMonitors"
        payload = "api_key=" + i + "&format=json&logs=1&all_time_uptime_ratio=1"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url2, data=payload, headers=headers)
        txt = response.json()
        get_pod = csv.writer(open("GetMonitor.csv", 'a'))
        get_pod.writerow(txt["monitors"][0])
        for line in txt['monitors']:
            name = line["friendly_name"]
            txt = re.search(r'POD_(.*?)_', name).group(1)
            # print(txt)
            per = line["all_time_uptime_ratio"]
            percentage = round(float(per), 2)
            # print(percentage)
            todo = {"uptime_ratio": percentage}
            response = call_rest_api(request_type='patch', endpoint=PODAPI_SERVER_ADDRESS + 'pods/' + str(txt) + '?verbose=true', data=json.dumps(todo))
            for item in response["records"]:
                print(item["id"])
                print(item["uptime_ratio"])
                time.sleep(.3)
            down_m = line.values()
            get_pod.writerow(down_m)
        time.sleep(1)
    print("data successfully added to CSV File")


def migrate_down_monitor():
    for i in range(len(M_url)):
        url_ = "https://api.uptimerobot.com/v2/newMonitor"
        payload2 = "api_key=" + POD1 + "&format=json&type=2&url=" + str(M_url[i]) + "&friendly_name=" + str(M_Friendly_Name[i]) + "&keyword_type=2&keyword_value=Device Up&keyword_case_type=1&alertcontact>type=qa4@qikpod.com"
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url_, data=payload2, headers=headers)
        txt = response.json()
        time.sleep(8)
        if txt["stat"] == "fail":
            print("Failed to create Monitor")
            print(response.json())
            print("https://uptimerobot.com/dashboard#mainDashboard")
            time.sleep(6)
    print("Go to Uptime and Check its Created : https://uptimerobot.com/dashboard#mainDashboard")


def delete_extra_monitor():
    for i in api_key:
        for j in non_match_id:
            url3 = "https://api.uptimerobot.com/v2/deleteMonitor"
            payload = "api_key=" + i + "&format=json&id=" + str(j)
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/x-www-form-urlencoded"
            }
            response = requests.request("POST", url3, data=payload, headers=headers)
            print(response.text)
            time.sleep(2)
    print("Go to Uptime and Check its Deleted :---> https://uptimerobot.com/dashboard#mainDashboard")


def check_up_monitor(key):
    url2 = "https://api.uptimerobot.com/v2/getMonitors"
    payload = "api_key=" + key + "&format=json&logs=1&all_time_uptime_ratio=1&response_times_start_date=" + str(hours_6)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url2, data=payload, headers=headers)
    txt = response.json()
    for line in txt['monitors']:
        # print(line["logs"][0])
        if '100' in line["all_time_uptime_ratio"]:
            # print(line["all_time_uptime_ratio"])
            id_ = line["id"]
            name = line["friendly_name"]
            url_ = line["url"]
            M_url.append(url_)
            M_Friendly_Name.append(name)
            m_id_list.append(id_)
    print(M_Friendly_Name)
    print(len(M_url))


def migrate_up_monitor(key):
    for i in range(len(M_url)):
        url_ = "https://api.uptimerobot.com/v2/newMonitor"
        payload2 = "api_key=" + key + "&format=json&type=2&url=" + str(M_url[i]) + "&friendly_name=" + str(M_Friendly_Name[i]) + "&keyword_type=2&keyword_value=Device Up&keyword_case_type=1&alertcontact>type=qa4@qikpod.com"
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url_, data=payload2, headers=headers)
        txt = response.json()
        print(txt)
        time.sleep(10)
    print("Go to Uptime and Check its Created : https://uptimerobot.com/dashboard#mainDashboard")


def delete_monitor():
    for i in m_id_list:
        url3 = "https://api.uptimerobot.com/v2/deleteMonitor"
        payload = "api_key=" + POD1 + "&format=json&id=" + str(i)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url3, data=payload, headers=headers)
        print(response.text)
        time.sleep(2)
    print("Go to Uptime and Check its Deleted :---> https://uptimerobot.com/dashboard#mainDashboard")


def find_extra_monitor():
    l1 = []
    duplicate = []
    for i in get_name:
        if i not in l1:
            l1.append(i)
        else:
            duplicate.append(i)
    print(duplicate)


get_pod_details()
get_all_monitor()
# pod_status()
# add_monitor(0, 50, POD2)
# add_monitor(51, 101, POD3)
# add_monitor(101, len(url), POD4)
find_new_pod_monitor()
add_new_find_monitor()
delete_extra_monitor()
down_pod_monitor()
migrate_down_monitor()
time.sleep(10)
check_up_monitor(POD1)
time.sleep(10)
delete_monitor()
find_extra_monitor()
