#!/usr/bin/env python3
"""
Test script for improved overlap prevention in multi-dimensional word cloud
"""

import math

def test_improved_positioning():
    """Test the improved positioning system with better spacing"""
    
    # Simulate the improved positioning algorithm
    placed_words = []
    max_words = 35
    base_spacing = 25
    
    def calculate_word_dimensions(word, font_size):
        # Conservative dimension estimation from the improved algorithm
        avg_char_width = font_size * 0.5
        word_width = max(len(word) * avg_char_width, font_size * 1.5)
        word_height = font_size * 0.9
        return {"width": word_width, "height": word_height}
    
    def find_valid_position(word, font_size, center_x=400, center_y=300, container_width=800, container_height=600):
        max_attempts = 150
        attempts = 0
        
        dimensions = calculate_word_dimensions(word, font_size)
        word_width = dimensions["width"]
        word_height = dimensions["height"]
        
        spacing_multiplier = 1 + (len(placed_words) * 0.1)
        current_spacing = base_spacing * spacing_multiplier
        
        while attempts < max_attempts:
            x, y = 0, 0
            
            if len(placed_words) == 0:
                x = center_x
                y = center_y
            else:
                word_index = len(placed_words)
                
                if attempts < 50:
                    # Spiral with generous spacing
                    angle = (word_index * 137.5) * (math.pi / 180)
                    radius = math.sqrt(word_index) * current_spacing + (attempts * 2)
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                elif attempts < 100:
                    # Grid with large spacing
                    grid_size = current_spacing * 2 + (attempts - 50) * 3
                    grid_x = (word_index % 8 - 4) * grid_size + center_x
                    grid_y = (word_index // 8 - 3) * grid_size + center_y
                    x = grid_x
                    y = grid_y
                else:
                    # Large radius positioning
                    radius = current_spacing * 3 + (attempts - 100) * 4
                    angle = (word_index * 45 + attempts * 20) * (math.pi / 180)
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
            
            # Conservative bounds checking
            margin = max(word_width, word_height) / 2 + current_spacing
            if x < margin or x > container_width - margin or y < margin or y > container_height - margin:
                attempts += 1
                continue
            
            # Simple distance-based collision avoidance
            too_close = False
            for placed in placed_words:
                dx = abs(x - placed["x"])
                dy = abs(y - placed["y"])
                min_distance = (word_width + placed["width"]) / 2 + current_spacing
                
                if dx < min_distance and dy < min_distance:
                    too_close = True
                    break
            
            if not too_close:
                return {"x": x, "y": y, "width": word_width, "height": word_height}
            
            attempts += 1
        
        # Fallback with large spacing
        return {
            "x": center_x + (len(placed_words) * 40) % 500 - 250,
            "y": center_y + (len(placed_words) * 35) % 400 - 200,
            "width": word_width,
            "height": word_height
        }
    
    # Test words with various lengths and frequencies
    test_words = [
        ("Python", 45), ("JavaScript", 40), ("React", 35), ("Database", 38),
        ("Algorithm", 42), ("Machine Learning", 48), ("Web Development", 44),
        ("Cloud Computing", 46), ("Artificial Intelligence", 52), ("Data Science", 41),
        ("Mobile App", 36), ("Backend", 32), ("Frontend", 34), ("DevOps", 30),
        ("Cybersecurity", 40), ("Blockchain", 35), ("IoT", 25), ("Big Data", 38),
        ("Microservices", 42), ("API", 28), ("Testing", 33), ("Deployment", 37),
        ("Scalability", 39), ("Performance", 36), ("User Experience", 41),
        ("Agile", 29), ("Scrum", 27), ("Version Control", 39), ("Docker", 31),
        ("Kubernetes", 37), ("AWS", 26), ("Azure", 28), ("GraphQL", 32),
        ("TypeScript", 36), ("Node.js", 33), ("Express.js", 35)
    ]
    
    print("Testing Improved Overlap Prevention Algorithm")
    print("=" * 50)
    
    successful_placements = 0
    total_attempts = 0
    
    for i, (word, font_size) in enumerate(test_words[:max_words]):
        position = find_valid_position(word, font_size)
        
        if position:
            placed_words.append({
                "x": position["x"],
                "y": position["y"],
                "width": position["width"],
                "height": position["height"],
                "word": word
            })
            successful_placements += 1
            print(f"✓ '{word}' placed at ({position['x']:.1f}, {position['y']:.1f}) size: {position['width']:.1f}x{position['height']:.1f}")
        else:
            print(f"✗ '{word}' could not be placed")
        
        total_attempts += 1
    
    # Check for overlaps in final placement
    overlaps = 0
    for i, word1 in enumerate(placed_words):
        for j, word2 in enumerate(placed_words):
            if i < j:  # Avoid checking the same pair twice
                dx = abs(word1["x"] - word2["x"])
                dy = abs(word1["y"] - word2["y"])
                min_distance_x = (word1["width"] + word2["width"]) / 2
                min_distance_y = (word1["height"] + word2["height"]) / 2
                
                if dx < min_distance_x and dy < min_distance_y:
                    overlaps += 1
                    print(f"Overlap detected: '{word1['word']}' and '{word2['word']}'")
    
    print(f"\nResults:")
    print(f"Total words processed: {total_attempts}")
    print(f"Successful placements: {successful_placements}")
    print(f"Success rate: {(successful_placements/total_attempts)*100:.1f}%")
    print(f"Overlaps detected: {overlaps}")
    print(f"Overlap rate: {(overlaps/max(1, successful_placements))*100:.1f}%")
    
    # Verify spacing improvements
    avg_spacing = sum(
        math.sqrt((word1["x"] - word2["x"])**2 + (word1["y"] - word2["y"])**2)
        for i, word1 in enumerate(placed_words)
        for j, word2 in enumerate(placed_words)
        if i < j
    ) / max(1, len(placed_words) * (len(placed_words) - 1) / 2)
    
    print(f"Average spacing between words: {avg_spacing:.1f}px")
    
    return successful_placements, overlaps, avg_spacing

if __name__ == "__main__":
    test_improved_positioning()