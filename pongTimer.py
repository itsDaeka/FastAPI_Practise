import requests
import time

url = "http://127.0.0.1:8000/ping"

start = time.perf_counter()
response = requests.get(url)
end = time.perf_counter()

latency_ms = (end - start) * 1000
print(f"Ping latency: {latency_ms:.2f} ms")
print("Response:", response.json())
