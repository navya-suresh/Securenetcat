/* Author: Navya G Suresh
import json
import requests
import csv

IPS = ["152.1.0.0/16", "152.7.0.0/16"]
API_URL = "https://censys.io/api/v1/data"
SEARCH_URL =  "https://censys.io/api/v1/search/ipv4"
#UID = ""
UID = ""
#SECRET = ""
SECRET = ""
def authenticate():
    res = requests.get(API_URL, auth=(UID, SECRET))
    print(res.status_code)
    print(res.json())

def search_data(IP):
    #for i in range(1,10):
    req_body = {
        "query": f"ip:{IP}",
        "page": 1,
        "fields": ["ip", "autonomous_system.asn", "autonomous_system.name", "autonomous_system.routed_prefix", "protocols", "metadata.os", "location.country", "443.https.ssl_3.support"],
        "flatten": True
        }
    res = requests.post(SEARCH_URL, auth=(UID, SECRET), json=req_body, headers={'Content-Type': 'application/json'}, verify=False)
    print(res.status_code)
    print(res.json())
    if res.status_code != 200:
        print("Status code returned - %s", res.status_code)
    return res.json()

def get_all_results():
    global IPS
    results = []   
    for IP in IPS:
        data = search_data(IP)
        results.append(data)
    return results

def write_to_json(report_data):
    with open('report.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=4)

def json_to_csv():
    with open('report.json') as json_file:
        data = json.load(json_file)
    result_file = open('result_file.csv', 'w', newline='')
    keys = []
    header = None
    header_written = False
    csv_writer = csv.writer(result_file)
    for data_item in data:
        results = data_item['results']
        for v in results:
            if not v.get('metadata.os'):
                v['metadata.os'] = ""
            if not header_written:
                header = v.keys()
                csv_writer.writerow(header)
                header_written = True
            csv_writer.writerow(get_values(header, v))
    result_file.close()

def get_values(header, row):
    values = []
    for key in header:
        values.append(row.get(key))
    return values


if __name__ == "__main__":
    #authenticate()
    output_data = get_all_results()
    write_to_json(output_data)
    json_to_csv()



