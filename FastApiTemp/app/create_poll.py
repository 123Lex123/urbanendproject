import requests

url = "http://127.0.0.1:8000/polls/"

data = {
    "question": "Какой ваш любимый ЯП?",
    "options": [
        {"text": "Python"},
        {"text": "JavaScript"},
        {"text": "Java"},
        {"text": "C++"}
    ]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Poll created successfully!")
    print("Response data:", response.json())
else:
    print("Failed to create poll.")
    print("Status code:", response.status_code)
    print("Response text:", response.text)
