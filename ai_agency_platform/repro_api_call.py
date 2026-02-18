import requests
import json

url = "http://localhost:8002/run-agency"
payload = {
    "prompt": "Draft a Service Agreement for a software consulting project.",
    "agency_type": "legal"
}

try:
    response = requests.post(url, json=payload)
    data = response.json()
    
    print("Status:", data.get("status"))
    print("\n--- Output Keys ---")
    print(data.get("output", {}).keys())
    
    print("\n--- Last Message ---")
    if data.get("messages"):
        print(data["messages"][-1])
    else:
        print("No messages found.")
        
    print("\n--- Document Snippet (from output) ---")
    if "document" in data.get("output", {}):
        print(data["output"]["document"][:200])
    else:
        print("No document in output.")

except Exception as e:
    print(f"Error: {e}")
