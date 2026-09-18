import requests
import json
import numpy as np

token = input("Notion token: ")
data_sourceID = "095ae770-cc10-8390-b5c6-07b81c93f683"
url = "https://api.notion.com/v1/data_sources/095ae770-cc10-8390-b5c6-07b81c93f683/query"
headers = {
    "Notion-Version": "2026-03-11",
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "sorts": [{ "property": "dato", "direction": "ascending"}]
}

def readDatabase(headers):
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()
    # kode 200 er good
    print(response.status_code)

    # kun for å se dataene:
    # with open('./test.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)
    return data

data = readDatabase(headers)
courseNames = list(list(data.values())[1][0].get('properties').keys())
if 'dato' in courseNames:
    courseNames.remove('dato')
if 'tittel' in courseNames:
    courseNames.remove('tittel')
print(courseNames)
numberOfCourses = len(courseNames)

numberOfDays = len(list(data.values())[1])

for day in range(0, numberOfDays):
    for course in courseNames:
        text = list(data.values())[1][day].get('properties').get(course).get('rich_text')
        if text is None or not any(text):
            print(f"jobbet ikke med {course} idag")
        else:
            time_string = list(text)[0].get('plain_text')
            print(f"jobbet {time_string} med {course}")
    print("#################################################################################")