"""
Test script for the Find Nearby Doctors feature
This script tests the /find-doctors endpoint
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
FIND_DOCTORS_ENDPOINT = "/find-doctors"

# Test data - Sample coordinates (New York City)
test_location = {
    "latitude": 40.7128,
    "longitude": -74.0060
}

def test_find_doctors():
    """Test the find doctors endpoint"""
    print("🧪 Testing Find Nearby Doctors Feature")
    print("=" * 60)
    
    url = BASE_URL + FIND_DOCTORS_ENDPOINT
    
    print(f"\n📍 Testing with location: {test_location}")
    print(f"🌐 Sending POST request to: {url}")
    
    try:
        response = requests.post(
            url,
            json=test_location,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\n📊 Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Request successful!")
            print(f"\n📋 Response Data:")
            print(json.dumps(data, indent=2))
            
            if data.get('success'):
                doctors = data.get('doctors', [])
                print(f"\n🏥 Found {len(doctors)} doctors/clinics:")
                print("-" * 60)
                
                for i, doctor in enumerate(doctors, 1):
                    print(f"\n{i}. {doctor.get('name')}")
                    print(f"   📍 Address: {doctor.get('address')}")
                    print(f"   📞 Phone: {doctor.get('phone')}")
                    print(f"   ⭐ Rating: {doctor.get('rating')}/5.0")
                    print(f"   📏 Distance: {doctor.get('distance')}")
                    print(f"   🏥 Type: {doctor.get('type')}")
                    print(f"   🕐 Open Now: {'Yes' if doctor.get('open_now') else 'No'}")
                
                print("\n" + "=" * 60)
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Response indicates failure")
                return False
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server")
        print("💡 Make sure Flask app is running on http://localhost:5000")
        print("   Run: python main.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_invalid_request():
    """Test with invalid data"""
    print("\n\n🧪 Testing with Invalid Data (Missing Coordinates)")
    print("=" * 60)
    
    url = BASE_URL + FIND_DOCTORS_ENDPOINT
    
    try:
        response = requests.post(
            url,
            json={},  # Empty data
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Response Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Correctly rejected invalid request!")
            data = response.json()
            print(f"Error message: {data.get('error')}")
            return True
        else:
            print(f"❌ Expected status 400, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n" + "🏥" * 30)
    print("  FIND NEARBY DOCTORS - ENDPOINT TESTING")
    print("🏥" * 30 + "\n")
    
    # Test 1: Valid request
    test1_passed = test_find_doctors()
    
    # Test 2: Invalid request
    test2_passed = test_invalid_request()
    
    # Summary
    print("\n\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Test 1 (Valid Request):   {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (Invalid Request): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
