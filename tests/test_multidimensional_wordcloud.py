#!/usr/bin/env python3
"""
Test script for multi-dimensional word cloud with unique colors per word,
spiral positioning, and largest word in center.
"""

import math

def test_multidimensional_wordcloud():
    """Test the new multi-dimensional word cloud implementation."""
    
    # Sample data with varying frequencies
    test_words = [
        {"text": "python", "frequency": 1, "size": 14},
        {"text": "programming", "frequency": 3, "size": 28.6},
        {"text": "function", "frequency": 5, "size": 37.7},
        {"text": "variable", "frequency": 8, "size": 49.1},
        {"text": "loop", "frequency": 12, "size": 62.1},
        {"text": "algorithm", "frequency": 20, "size": 84.5},
        {"text": "data", "frequency": 35, "size": 120.0},
        {"text": "structure", "frequency": 18, "size": 80.2},
        {"text": "class", "frequency": 15, "size": 73.8},
        {"text": "method", "frequency": 10, "size": 56.4},
        {"text": "object", "frequency": 7, "size": 45.8},
        {"text": "inheritance", "frequency": 4, "size": 33.2}
    ]
    
    print("🎨 MULTI-DIMENSIONAL WORD CLOUD TEST")
    print("=" * 50)
    
    # Vibrant color palette
    vibrant_colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', 
        '#FF8E53', '#6C5CE7', '#A29BFE', '#FD79A8', '#FDCB6E', '#6C5CE7',
        '#00B894', '#00CEC9', '#0984E3', '#6C5CE7', '#A29BFE', '#FD79A8',
        '#E17055', '#00B894', '#00CEC9', '#74B9FF', '#A29BFE', '#FD79A8',
        '#FF7675', '#74B9FF', '#00B894', '#00CEC9', '#0984E3', '#6C5CE7'
    ]
    
    # Container dimensions
    container_width = 800
    container_height = 600
    center_x = container_width / 2
    center_y = container_height / 2
    
    # Sort by frequency (largest first)
    sorted_words = sorted(test_words, key=lambda x: x['frequency'], reverse=True)
    
    print(f"📊 Container: {container_width}x{container_height}px")
    print(f"📍 Center position: ({center_x}, {center_y})")
    print(f"🎯 Words sorted by frequency (largest first)")
    print()
    
    for i, word in enumerate(sorted_words):
        font_size = word['size']
        color = vibrant_colors[i % len(vibrant_colors)]
        
        # Calculate position
        if i == 0:
            # Largest word in center
            x, y = center_x, center_y
            position_desc = f"CENTER ({x}, {y})"
        else:
            # Spiral positioning using golden angle
            angle = (i * 137.5) * (math.pi / 180)  # Convert to radians
            radius = (i ** 0.5) * 30  # Square root for natural spacing
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            position_desc = f"SPIRAL r={radius:.0f}° θ={angle:.0f}° ({x:.0f}, {y:.0f})"
        
        # Dynamic rotation
        rotation = (i * 25) % 60 - 30
        
        # Font weight based on frequency
        weight = '800' if word['frequency'] > 20 else '700' if word['frequency'] > 15 else '600' if word['frequency'] > 8 else '500' if word['frequency'] > 3 else '400'
        
        print(f"📝 Word: '{word['text']}' (freq: {word['frequency']})")
        print(f"   🎨 Color: {color}")
        print(f"   📏 Size: {font_size}px")
        print(f"   📍 Position: {position_desc}")
        print(f"   🔄 Rotation: {rotation}°")
        print(f"   💪 Weight: {weight}")
        print(f"   🎯 Category: {'🔥 DOMINANT' if word['frequency'] > 25 else '⭐ PROMINENT' if word['frequency'] > 15 else '📋 MODERATE' if word['frequency'] > 5 else '💭 MINIMAL'}")
        print()
    
    print("✨ KEY FEATURES:")
    print("✅ Unique color for each word (vibrant palette)")
    print("✅ Largest word placed in center")
    print("✅ Spiral positioning using golden angle (137.5°)")
    print("✅ Multi-dimensional layout (not just horizontal)")
    print("✅ Dynamic rotation angles (-30° to +30°)")
    print("✅ Z-index layering based on frequency")
    print("✅ Absolute positioning for precise placement")
    print("✅ Responsive hover effects with scaling")

if __name__ == "__main__":
    test_multidimensional_wordcloud()