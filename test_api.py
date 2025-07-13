import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("api_key")
print(f"API Key: {api_key}")

# Test API call
if api_key:
    test_url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=imperial"
    print(f"Test URL: {test_url}")
    
    response = requests.get(test_url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ API key is working!")
        data = response.json()
        print(f"Temperature in London: {data['main']['temp']}°F")
    else:
        print(f"❌ API call failed: {response.status_code}")
        print(f"Response: {response.text}")
else:
    print("❌ No API key found in environment variables")
