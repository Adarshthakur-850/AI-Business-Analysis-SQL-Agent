import requests
import json

url = "http://127.0.0.1:8001/ask"

payload = {
    "question": "Which customer has the most orders?"
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Failed to connect: {e}")
