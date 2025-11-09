#!/usr/bin/env python3
"""
Test live font sizes from the API to verify minimum size increase
"""

import requests
import json
import sys

def test_live_font_sizes():
    """Test the actual API response for font sizes"""
    print("🔍 Testing Live Font Sizes from API")
    print("=" * 50)
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First, visit the login page to get session cookies
        login_response = session.get('http://localhost:5000/login')
        print(f"📱 Login page status: {login_response.status_code}")
        
        # Now try the API endpoint
        api_response = session.get('http://localhost:5000/api/word_cloud/4/data')
        print(f"🌐 API response status: {api_response.status_code}")
        
        if api_response.status_code == 200:
            try:
                data = api_response.json()
                print(f"📊 Retrieved {len(data)} words from API")
                
                # Find words with different frequencies
                min_size = float('inf')
                max_size = 0
                min_word = ""
                max_word = ""
                
                print("\n📝 Sample words and their sizes:")
                print("-" * 40)
                
                for word_data in data[:10]:  # Show first 10 words
                    word = word_data.get('text', 'Unknown')
                    size = word_data.get('size', 0)
                    frequency = word_data.get('frequency', 0)
                    
                    print(f"'{word}': {size}px (freq: {frequency})")
                    
                    # Track min/max
                    if size < min_size:
                        min_size = size
                        min_word = word
                    if size > max_size:
                        max_size = size
                        max_word = word
                
                print(f"\n📏 Size Range:")
                print(f"   Minimum: {min_size}px ('{min_word}')")
                print(f"   Maximum: {max_size}px ('{max_word}')")
                
                # Verify minimum size is 18px or larger
                if min_size >= 18:
                    print(f"\n✅ SUCCESS: Minimum font size is {min_size}px (≥18px)")
                    print("✅ Small words are now larger and more readable!")
                else:
                    print(f"\n⚠️  WARNING: Minimum font size is {min_size}px (<18px)")
                    
                return True
                
            except json.JSONDecodeError:
                print(f"❌ Response is not JSON. Content: {api_response.text[:200]}")
                return False
        else:
            print(f"❌ API request failed. Status: {api_response.status_code}")
            print(f"Response: {api_response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_live_font_sizes()
    sys.exit(0 if success else 1)