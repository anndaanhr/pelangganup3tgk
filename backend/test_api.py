import requests
import json

BASE_URL = "http://localhost:8000/api/customers"

def test_endpoint(endpoint):
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {url}...")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            # Print first few items or summary
            print(json.dumps(data, indent=2)[:500] + "...") 
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    print("--- Checking Backend API ---")
    test_endpoint("/dashboard")
    test_endpoint("/dashboard/trends")
    test_endpoint("/dashboard/distribution")
