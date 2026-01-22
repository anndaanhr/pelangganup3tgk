import requests
import traceback

BASE_URL = "http://localhost:8000"

print("\n=== DEBUGGING TRAFFIC CRASHES (LIVE) ===")
print("Make sure the backend is running in another terminal!")

def test_endpoint(path):
    url = f"{BASE_URL}{path}"
    print(f"\n[TESTING] {url}")
    try:
        response = requests.get(url, timeout=10) # 10s timeout
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text[:500]}...")
        else:
            print(f"SUCCESS. Payload size: {len(response.content)} bytes")
    except Exception as e:
        print(f"CRASH/TIMEOUT DETECTED: {e}")

# 1. Test Trends
test_endpoint("/api/customers/dashboard/trends")

# 2. Test All Customers
test_endpoint("/api/customers/all/2025?page=1&page_size=10")

# 3. Test Lost Customers
test_endpoint("/api/customers/lost?page=1&page_size=10")

print("\n=== DEBUG COMPLETE ===")
