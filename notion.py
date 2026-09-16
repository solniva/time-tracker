import requests

url = "https://api.notion.com/v1/databases/3a2ae770cc108036a497d815efcae57b"

token = input("Notion token: ")
print(token)

headers = {
    "Notion-Version": "2026-03-11",
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)

print(response.text)