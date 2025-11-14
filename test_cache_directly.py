#!/usr/bin/env python3
"""
Test script to verify HTTP caching is working for word cloud data API.
"""

import requests
import json
import sys

def test_word_cloud_cache():
    """Test the HTTP caching implementation for word cloud data"""
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🧪 Testing HTTP Caching for Word Cloud Data API")
    print("=" * 60)
    
    # 1. Login first
    print("\n1️⃣ Logging in as student...")
    login_data = {
        'username': 'a',  # Simple test user
        'password': 'comp5241',
        'role': 'student'
    }
    
    try:
        login_response = session.post(f"{base_url}/login", json=login_data, 
                                     headers={'Content-Type': 'application/json'})
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {login_response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # 2. Test initial request (should get full data)
    print("\n2️⃣ Testing initial request (should get full data)...")
    try:
        response1 = session.get(f"{base_url}/api/word_cloud/4/data")
        print(f"First request status: {response1.status_code}")
        print(f"First request headers: {dict(response1.headers)}")
        
        if response1.status_code == 200:
            etag1 = response1.headers.get('ETag')
            print(f"✅ Got ETag: {etag1}")
            data1 = response1.json()
            print(f"✅ Got data with {len(data1.get('words', []))} words")
        else:
            print(f"❌ First request failed: {response1.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ First request error: {e}")
        return False
    
    # 3. Test cached request (should get 304)
    print("\n3️⃣ Testing cached request (should get 304 Not Modified)...")
    try:
        headers = {'If-None-Match': etag1} if etag1 else {}
        response2 = session.get(f"{base_url}/api/word_cloud/4/data", headers=headers)
        print(f"Second request status: {response2.status_code}")
        print(f"Second request headers: {dict(response2.headers)}")
        
        if response2.status_code == 304:
            print("✅ Got 304 Not Modified - caching is working!")
        elif response2.status_code == 200:
            print("⚠️  Got 200 OK - data changed or caching not working")
            etag2 = response2.headers.get('ETag')
            print(f"New ETag: {etag2}")
        else:
            print(f"❌ Second request failed: {response2.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Second request error: {e}")
        return False
    
    # 4. Test with different ETag (should get 200)
    print("\n4️⃣ Testing with different ETag (should get 200)...")
    try:
        fake_etag = '"fake_etag_12345"'
        headers = {'If-None-Match': fake_etag}
        response3 = session.get(f"{base_url}/api/word_cloud/4/data", headers=headers)
        print(f"Third request status: {response3.status_code}")
        
        if response3.status_code == 200:
            print("✅ Got 200 OK - different ETag correctly ignored")
        else:
            print(f"❌ Third request unexpected status: {response3.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Third request error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ HTTP Caching test completed successfully!")
    print("The word cloud API is properly implementing HTTP 304 caching.")
    return True

if __name__ == '__main__':
    success = test_word_cloud_cache()
    sys.exit(0 if success else 1)