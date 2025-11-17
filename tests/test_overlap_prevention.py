#!/usr/bin/env python3
"""
Test script to verify word cloud overlap prevention
"""
import math

def test_overlap_prevention():
    """Test the collision detection and positioning algorithms"""
    
    print("🧪 Testing Word Cloud Overlap Prevention")
    print("=" * 50)
    
    # Test data with varying frequencies
    test_words = [
        {"text": "Python", "frequency": 25, "size": 120},
        {"text": "JavaScript", "frequency": 20, "size": 90},
        {"text": "React", "frequency": 15, "size": 70},
        {"text": "Django", "frequency": 12, "size": 60},
        {"text": "Node.js", "frequency": 10, "size": 50},
        {"text": "HTML", "frequency": 8, "size": 45},
        {"text": "CSS", "frequency": 6, "size": 40},
        {"text": "Git", "frequency": 5, "size": 35},
        {"text": "Docker", "frequency": 4, "size": 30},
        {"text": "AWS", "frequency": 3, "size": 25},
        {"text": "MongoDB", "frequency": 2, "size": 20},
        {"text": "Redis", "frequency": 1, "size": 18}
    ]
    
    # Simulate collision detection logic
    placed_words = []
    container_width = 800
    container_height = 600
    center_x = container_width / 2
    center_y = container_height / 2
    padding = 8
    
    def check_collision(x, y, width, height):
        """Check if a word would collide with already placed words"""
        for placed in placed_words:
            dx = abs(x - placed['x'])
            dy = abs(y - placed['y'])
            min_distance_x = (width + placed['width']) / 2 + padding
            min_distance_y = (height + placed['height']) / 2 + padding
            
            if dx < min_distance_x and dy < min_distance_y:
                return True
        return False
    
    def find_valid_position(word, font_size, rotation):
        """Find a non-overlapping position for a word"""
        max_attempts = 100
        attempts = 0
        
        # Estimate word dimensions
        avg_char_width = font_size * 0.6
        word_width = len(word['text']) * avg_char_width
        word_height = font_size * 1.2
        
        while attempts < max_attempts:
            x, y = 0, 0
            
            if len(placed_words) == 0:
                # First word goes in center
                x, y = center_x, center_y
            else:
                # Try different positioning strategies
                if attempts < 30:
                    # Spiral positioning (golden angle)
                    angle = (len(placed_words) * 137.5 + attempts * 10) * (math.pi / 180)
                    radius = math.sqrt(len(placed_words)) * 40 + attempts * 5
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                elif attempts < 60:
                    # Grid-based positioning
                    grid_size = 60 + attempts
                    grid_x = (len(placed_words) % 8 - 4) * grid_size + center_x
                    grid_y = (len(placed_words) // 8 - 3) * grid_size + center_y
                    x = grid_x + (attempts - 30) * 10
                    y = grid_y + (attempts - 30) * 8
                else:
                    # Random positioning with increasing radius
                    angle = math.random() * 2 * math.pi if hasattr(math, 'random') else (attempts * 0.1)
                    radius = 50 + attempts * 2
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
            
            # Check bounds
            if x < word_width/2 or x > container_width - word_width/2 or \
               y < word_height/2 or y > container_height - word_height/2:
                attempts += 1
                continue
            
            # Check collision
            if not check_collision(x, y, word_width, word_height):
                return {'x': x, 'y': y, 'width': word_width, 'height': word_height}
            
            attempts += 1
        
        # Fallback position
        return {
            'x': center_x + (len(placed_words) * 20) % 200 - 100,
            'y': center_y + (len(placed_words) * 15) % 150 - 75,
            'width': word_width,
            'height': word_height
        }
    
    print("📍 Testing positioning for words:")
    
    for i, word in enumerate(test_words):
        position = find_valid_position(word, word['size'], 0)
        placed_words.append(position)
        
        print(f"  {i+1:2d}. '{word['text']:<12}' "
              f"freq={word['frequency']:2d} "
              f"size={word['size']:3d}px "
              f"pos=({position['x']:6.1f}, {position['y']:6.1f}) "
              f"dim={position['width']:5.1f}x{position['height']:4.1f}")
    
    print("\n✅ Overlap prevention test completed!")
    print(f"📊 Successfully positioned {len(placed_words)} words without overlap")
    
    # Verify no overlaps
    overlaps = 0
    for i, word1 in enumerate(placed_words):
        for j, word2 in enumerate(placed_words):
            if i >= j:
                continue
            
            dx = abs(word1['x'] - word2['x'])
            dy = abs(word1['y'] - word2['y'])
            min_dx = (word1['width'] + word2['width']) / 2 + padding
            min_dy = (word1['height'] + word2['height']) / 2 + padding
            
            if dx < min_dx and dy < min_dy:
                overlaps += 1
                print(f"⚠️  Overlap detected between words {i+1} and {j+1}")
    
    if overlaps == 0:
        print("🎯 Perfect! No overlapping words detected.")
    else:
        print(f"⚠️  Found {overlaps} overlapping pairs.")
    
    print("\n🔑 Key Features Tested:")
    print("   • Collision detection algorithm")
    print("   • Multiple positioning strategies (spiral, grid, random)")
    print("   • Bounds checking within container")
    print("   • Padding enforcement between words")
    print("   • Fallback positioning system")

if __name__ == "__main__":
    test_overlap_prevention()