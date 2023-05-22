import requests

ride = {
    "PULocationID": 10,
    "DOLocationID": 50,
    "trip_distance": 40
}

url = 'http://localhost:9696/predict'
print((f"URL: {url}"))
response = requests.post(url, json=ride)
print(response.json())
