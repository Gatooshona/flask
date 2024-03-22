import requests

response = requests.post('http://127.0.0.1:5000/notices',
                         json={'title': 'one', 'owner_name': 'Oksana'},)
print(response.status_code)
print(response.text)


# response = requests.get('http://127.0.0.1:5000/notices/1',)
# print(response.status_code)
# print(response.text)


# response = requests.post('http://127.0.0.1:5000/notices',
#                          json={'title': 'two', 'owner_name': 'Oksana'},)
# print(response.status_code)
# print(response.text)
