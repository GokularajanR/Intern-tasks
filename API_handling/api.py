import requests

URL = "https://my-json-server.typicode.com/gulugulu2042/Intern-tasks/content"

response = requests.get(URL)
print(response.text)

response = requests.get(f"{URL}/31")
print(response.json())

#CHANGES WILL NOT BE REFLECTED
#------------------------------------------------
new_post = {"id": 16, "name": "Yuva"}
response = requests.post(URL, json=new_post)
print(response.json())

updated_post = {"id": 31, "name": "Updated Post"}
response = requests.put(f"{URL}/31", json=updated_post)
print(response.json())

response = requests.delete(f"{URL}/31")
print("DELETE Response:", response.status_code)
#------------------------------------------------