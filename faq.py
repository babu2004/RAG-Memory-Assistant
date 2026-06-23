import requests
import json
doc_url = "https://datatalks.club/faq/json/courses.json"
response = requests.get(doc_url)
raw_course = response.json()

#print(raw_course[0])

documents = []
base_url = "https://datatalks.club/faq"
for course in raw_course:

    course_url = f"{base_url}{course['path']}"
    course_response = requests.get(course_url)
    course_response.raise_for_status()
    course_data = course_response.json()

    documents.extend(course_data)
print(len(documents))
print(documents[0])

filename = "faq.json"

# with open(filename,"w",encoding="utf-8") as json_file:
#     json.dump(documents,json_file,indent = 4)
# print("faq.json was created!!!")
