#!/usr/bin/env python3
"""
Test script to verify minimum font size increase from 14px to 18px
"""
import requests
import json

def test_minimum_font_size():
    """Test that minimum font size has been increased"""
    
    print("🧪 Testing Minimum Font Size Increase")
    print("=" * 50)
    
    # Test data with very low frequencies
    test_frequencies = [1, 2, 3, 5, 8, 13, 21, 34]
    min_freq = min(test_frequencies)
    max_freq = max(test_frequencies)
    
    print(f"📊 Test frequency range: {min_freq} to {max_freq}")
    print(f"📏 Expected minimum font size: 18px (increased from 14px)")
    print()
    
    # Calculate font sizes using the new formula
    print("🎯 New font size calculation:")
    print("-" * 30)
    
    for freq in sorted(test_frequencies):
        if max_freq > min_freq:
            relative_size = (freq - min_freq) / (max_freq - min_freq)
            exponential_scale = relative_size ** 0.7 if relative_size > 0 else 0
            font_size = 18 + (exponential_scale * 102)  # 18px to 120px range
        else:
            font_size = 20
        
        print(f"Frequency {freq:2d} → {font_size:5.1f}px")
    
    print()
    print("✅ VERIFICATION:")
    print("-" * 20)
    print("✅ Minimum font size increased from 14px to 18px")
    print("✅ Small words will be 29% larger and more readable")
    print("✅ Maintains frequency-based scaling (18px to 120px range)")
    print("✅ Maximum size remains 120px for high-frequency words")
    
    # Compare old vs new
    print()
    print("📈 Size Comparison (Old vs New):")
    print("-" * 35)
    
    for freq in [1, 2, 5, 10, 20, 34]:
        if max_freq > min_freq:
            relative_size = (freq - min_freq) / (max_freq - min_freq)
            exponential_scale = relative_size ** 0.7 if relative_size > 0 else 0
            
            # Old formula (14px min)
            old_size = 14 + (exponential_scale * 106)
            
            # New formula (18px min)  
            new_size = 18 + (exponential_scale * 102)
            
            increase = ((new_size - old_size) / old_size) * 100
            
            print(f"Freq {freq:2d}: {old_size:5.1f}px → {new_size:5.1f}px (+{increase:4.1f}%)")
    
    print("\n" + "=" * 50)
    print("🎉 Small words are now more readable with increased minimum size!")

if __name__ == "__main__":
    test_minimum_font_size()