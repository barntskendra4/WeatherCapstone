"""
Test script to verify API error handling
"""

import os
from core.weather_api import WeatherAPI, WeatherAPIError

def test_no_api_key():
    """Test what happens when no API key is provided"""
    print("Testing no API key scenario...")
    try:
        # Temporarily remove API key from environment
        old_key = os.environ.get('api_key')
        if 'api_key' in os.environ:
            del os.environ['api_key']
        
        api = WeatherAPI(None)
        print("❌ Should have raised WeatherAPIError")
        
    except WeatherAPIError as e:
        print(f"✅ Correctly caught WeatherAPIError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")
    finally:
        # Restore API key if it existed
        if old_key:
            os.environ['api_key'] = old_key

def test_invalid_api_key():
    """Test what happens with an invalid API key"""
    print("\nTesting invalid API key scenario...")
    try:
        # Test with invalid key format
        api = WeatherAPI("invalid_key")
        print("❌ Should have raised WeatherAPIError")
        
    except WeatherAPIError as e:
        print(f"✅ Correctly caught WeatherAPIError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")

def test_empty_api_key():
    """Test what happens with an empty API key"""
    print("\nTesting empty API key scenario...")
    try:
        api = WeatherAPI("")
        print("❌ Should have raised WeatherAPIError")
        
    except WeatherAPIError as e:
        print(f"✅ Correctly caught WeatherAPIError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")

def test_whitespace_api_key():
    """Test what happens with whitespace-only API key"""
    print("\nTesting whitespace API key scenario...")
    try:
        api = WeatherAPI("   ")
        print("❌ Should have raised WeatherAPIError")
        
    except WeatherAPIError as e:
        print(f"✅ Correctly caught WeatherAPIError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("Testing Weather API Error Handling")
    print("=" * 50)
    
    test_no_api_key()
    test_invalid_api_key()
    test_empty_api_key()
    test_whitespace_api_key()
    
    print("\n" + "=" * 50)
    print("Error handling tests completed!")
