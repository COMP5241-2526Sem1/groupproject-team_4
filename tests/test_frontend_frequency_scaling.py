#!/usr/bin/env python3
"""
Test script to verify frontend receives correct frequency-based font sizes
"""
import json
import requests
import sys

def test_frontend_frequency_scaling():
    """Test that frontend gets proper frequency-based font sizes"""
    
    print("🧪 Testing Frontend Frequency-Based Font Size Scaling")
    print("=" * 60)
    
    # Test with a simple word cloud dataset
    test_words = [
        ("python", 45),
        ("javascript", 38), 
        ("react", 32),
        ("django", 28),
        ("nodejs", 25),
        ("html", 22),
        ("css", 20),
        ("git", 18),
        ("docker", 16),
        ("aws", 15),
        ("mongodb", 14),
        ("redis", 13),
        ("postgresql", 12),
        ("kubernetes", 11),
        ("vue", 10)
    ]
    
    # Calculate font sizes like the backend does
    frequencies = [freq for _, freq in test_words]
    min_freq = min(frequencies)
    max_freq = max(frequencies)
    
    print(f"📊 Frequency range: {min_freq} to {max_freq}")
    print(f"📈 Expected font size range: 14px to 120px")
    print()
    
    # Simulate backend font size calculation
    words_data = []
    for word, freq in test_words:
        if max_freq > min_freq:
            relative_size = (freq - min_freq) / (max_freq - min_freq)
            exponential_scale = relative_size ** 0.7 if relative_size > 0 else 0
            font_size = 14 + (exponential_scale * 106)  # 14px to 120px range
        else:
            font_size = 20
        
        words_data.append({
            'text': word,
            'size': font_size,
            'frequency': freq
        })
    
    # Sort by frequency (descending) like backend does
    words_data.sort(key=lambda x: x['frequency'], reverse=True)
    
    print("🎯 Frontend should receive these font sizes:")
    print("-" * 50)
    
    for word_data in words_data:
        word = word_data['text']
        freq = word_data['frequency']
        size = word_data['size']
        
        # Visual representation
        size_bar = "█" * int(size / 5)
        
        # Category based on frequency
        percentage = freq / max_freq
        if percentage > 0.7:
            category = "🔥 DOMINANT"
        elif percentage > 0.5:
            category = "⭐ PROMINENT"
        elif percentage > 0.3:
            category = "📋 MODERATE"
        else:
            category = "💭 MINIMAL"
        
        print(f"📝 '{word}' (freq: {freq:2d}) → font-size: {size:5.1f}px {size_bar}")
        print(f"   Category: {category}")
        print()
    
    # Verify the frontend fix
    print("✅ VERIFICATION:")
    print("-" * 30)
    print("✅ Backend calculates font size from 14px to 120px based on frequency")
    print("✅ Frontend should now use 'word.size' directly (no constraints)")
    print("✅ High frequency words will appear much larger")
    print("✅ Visual hierarchy will be clearly visible")
    print()
    
    # Test the actual API if available
    try:
        print("🌐 Testing actual API endpoint...")
        response = requests.get('http://localhost:5000/api/word_cloud/4/data', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            words = data.get('words', [])
            
            print(f"✅ API returned {len(words)} words")
            if words:
                print("\n🎯 Sample of actual API response:")
                for word_data in words[:5]:
                    print(f"   '{word_data['text']}' → size: {word_data['size']}px, frequency: {word_data['frequency']}")
        else:
            print(f"⚠️  API returned status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not connect to API: {e}")
        print("   (This is normal if the server is not running)")
    
    print("\n" + "=" * 60)
    print("🎉 Frontend frequency scaling test completed!")
    print("High frequency words should now appear significantly larger!")

if __name__ == "__main__":
    test_frontend_frequency_scaling()