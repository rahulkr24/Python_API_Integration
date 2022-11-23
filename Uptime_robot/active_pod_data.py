import csv

Friendly_Name = []
url = []
with open('/home/rahul/Desktop/Uptime/FIELD_PODS_ACTIVE.csv') as file_obj:
    heading = next(file_obj)
    reader_obj = csv.reader(file_obj)
    for data in reader_obj:
        new_pod_id = "POD_" + data[0] + "_" + data[1]
        Friendly_Name.append(new_pod_id)
        new_url = "https://appapi.qikpod.com:8989/status/" + data[0]
        url.append(new_url)
    print(Friendly_Name)
    print(url)
