import urllib.request
import json

data = json.dumps({
    "code": "def calculate_discount(price, discount_percent):\n    return price - discount_percent",
    "language": "python"
}).encode("utf-8")

req = urllib.request.Request(
    "http://127.0.0.1:8000/generate", 
    data=data, 
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as f:
        print(json.dumps(json.loads(f.read().decode("utf-8")), indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
