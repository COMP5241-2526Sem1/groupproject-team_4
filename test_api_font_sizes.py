#!/usr/bin/env python3
"""
Simple test to check the API response for font sizes
"""
import requests
import json

def test_api_font_sizes():
    """Test the actual API to see font sizes"""
    
    print("🧪 Testing API Font Sizes")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:5000/api/word_cloud/4/data', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            words = data.get('words', [])
            
            print(f"✅ API returned {len(words)} words")
            print()
            
            if words:
                print("🎯 Font sizes from API:")
                print("-" * 30)
                
                # Sort by frequency to see the scaling
                words_sorted = sorted(words, key=lambda x: x['frequency'], reverse=True)
                
                for word_data in words_sorted[:10]:  # Show top 10
                    word = word_data['text']
                    freq = word_data['frequency']
                    size = word_data['size']
                    
                    print(f"'{word}' (freq: {freq}) → font-size: {size:.1f}px")
                
                print()
                print("📊 Size Statistics:")
                sizes = [w['size'] for w in words]
                print(f"   Min size: {min(sizes):.1f}px")
                print(f"   Max size: {max(sizes):.1f}px")
                print(f"   Avg size: {sum(sizes)/len(sizes):.1f}px")
                
                # Check if we have good frequency scaling
                max_freq = max(w['frequency'] for w in words)
                min_freq = min(w['frequency'] for w in words)
                print(f"   Frequency range: {min_freq} to {max_freq}")
                
                if max(sizes) > 50:
                    print("✅ Good! High frequency words are getting large font sizes")
                else:
                    print("⚠️  High frequency words may not be large enough")
                    
        else:
            print(f"❌ API returned status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        print("   Make sure the Flask server is running")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    test_api_font_sizes()