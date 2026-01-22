import requests
import sys

print("STARTING_TEST")
try:
    # Test Root
    r = requests.get("http://localhost:8000/", timeout=2)
    print(f"ROOT: {r.status_code}")
    
    # Test Dashboard Data
    r = requests.get("http://localhost:8000/api/customers/dashboard", timeout=5)
    print(f"DASHBOARD: {r.status_code}")
    if r.status_code == 200:
        print(f"DATA: {r.text[:50]}")
    else:
        print(f"ERROR_MSG: {r.text}")
        
except Exception as e:
    print(f"EXCEPTION: {e}")
print("ENDING_TEST")
