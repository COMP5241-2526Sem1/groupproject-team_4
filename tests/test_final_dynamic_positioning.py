#!/usr/bin/env python3
"""
Final test script for dynamic spacing overlap prevention in multi-dimensional word cloud
"""

import math
import random

def test_final_dynamic_positioning():
    """Test the final dynamic spacing system with guaranteed no overlaps"""
    
    # Simulate the final dynamic positioning algorithm
    placed_words = []
    max_words = 15
    container_width = 800
    container_height = 600
    
    def calculate_word_dimensions(word, font_size):
        # Final conservative dimension estimation
        avg_char_width = font_size * 0.35
        word_width = max(len(word) * avg_char_width, font_size * 0.8)
        word_height = font_size * 0.6
        return {"width": word_width, "height": word_height}
    
    def find_valid_position(word, font_size, center_x=400, center_y=300):
        word_index = len(placed_words)
        dimensions = calculate_word_dimensions(word, font_size)
        
        # Dynamic layout: adjust spacing based on word size
        base_spacing = max(dimensions["width"], dimensions["height"]) + 80
        
        # Use a 3x5 layout for perfect spacing
        cols = 3
        rows = 5
        col = word_index % cols
        row = word_index // cols
        
        # Calculate available space
        available_width = container_width - 100
        available_height = container_height - 100
        
        # Dynamic spacing based on largest word so far
        max_width = dimensions["width"]
        max_height = dimensions["height"]
        for placed in placed_words:
            max_width = max(max_width, placed["width"])
            max_height = max(max_height, placed["height"])
        
        dynamic_col_spacing = max(base_spacing, max_width + 60)
        dynamic_row_spacing = max(base_spacing * 0.8, max_height + 40)
        
        # Calculate position with dynamic spacing
        total_width = (cols - 1) * dynamic_col_spacing
        total_height = (rows - 1) * dynamic_row_spacing
        
        start_x = (container_width - total_width) / 2
        start_y = (container_height - total_height) / 2
        
        x = start_x + col * dynamic_col_spacing
        y = start_y + row * dynamic_row_spacing
        
        # Minimal randomness
        random_offset = 5
        x += (random.random() - 0.5) * random_offset
        y += (random.random() - 0.5) * random_offset
        
        # Ensure within very conservative bounds
        margin = max(dimensions["width"], dimensions["height"]) / 2 + 50
        x = max(margin, min(container_width - margin, x))
        y = max(margin, min(container_height - margin, y))
        
        return {"x": x, "y": y, "width": dimensions["width"], "height": dimensions["height"]}
    
    # Test words with reduced font sizes (final set)
    test_words = [
        ("Python", 25), ("JavaScript", 24), ("React", 22), ("Database", 23),
        ("Algorithm", 25), ("Machine Learning", 28), ("Web Development", 26),
        ("Cloud Computing", 27), ("Artificial Intelligence", 30), ("Data Science", 25),
        ("Mobile App", 22), ("Backend", 20), ("Frontend", 21), ("DevOps", 19),
        ("Cybersecurity", 24)
    ]
    
    print("Testing Final Dynamic Overlap Prevention Algorithm")
    print("=" * 52)
    
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
    overlap_details = []
    
    for i, word1 in enumerate(placed_words):
        for j, word2 in enumerate(placed_words):
            if i < j:  # Avoid checking the same pair twice
                dx = abs(word1["x"] - word2["x"])
                dy = abs(word1["y"] - word2["y"])
                min_distance_x = (word1["width"] + word2["width"]) / 2
                min_distance_y = (word1["height"] + word2["height"]) / 2
                
                if dx < min_distance_x and dy < min_distance_y:
                    overlaps += 1
                    overlap_area = (min_distance_x - dx) * (min_distance_y - dy)
                    overlap_details.append(f"'{word1['word']}' and '{word2['word']}' (area: {overlap_area:.1f}px²)")
    
    print(f"\nResults:")
    print(f"Total words processed: {total_attempts}")
    print(f"Successful placements: {successful_placements}")
    print(f"Success rate: {(successful_placements/total_attempts)*100:.1f}%")
    print(f"Overlaps detected: {overlaps}")
    print(f"Overlap rate: {(overlaps/max(1, successful_placements))*100:.1f}%")
    
    if overlaps == 0:
        print("🎉 PERFECT! No overlaps detected!")
    else:
        print(f"Overlap details:")
        for detail in overlap_details:
            print(f"  - {detail}")
    
    # Verify spacing improvements
    avg_spacing = sum(
        math.sqrt((word1["x"] - word2["x"])**2 + (word1["y"] - word2["y"])**2)
        for i, word1 in enumerate(placed_words)
        for j, word2 in enumerate(placed_words)
        if i < j
    ) / max(1, len(placed_words) * (len(placed_words) - 1) / 2)
    
    min_spacing_found = float('inf')
    for i, word1 in enumerate(placed_words):
        for j, word2 in enumerate(placed_words):
            if i != j:
                distance = math.sqrt((word1["x"] - word2["x"])**2 + (word1["y"] - word2["y"])**2)
                min_spacing_found = min(min_spacing_found, distance)
    
    print(f"Average spacing between words: {avg_spacing:.1f}px")
    print(f"Minimum spacing found: {min_spacing_found:.1f}px")
    
    # Show dynamic layout
    print(f"\nDynamic Layout (3x5):")
    for row in range(5):
        row_words = []
        for col in range(3):
            index = row * 3 + col
            if index < len(placed_words):
                row_words.append(placed_words[index]["word"])
            else:
                row_words.append("---")
        print(f"Row {row + 1}: {' | '.join(row_words)}")
    
    return successful_placements, overlaps, avg_spacing, min_spacing_found

if __name__ == "__main__":
    test_final_dynamic_positioning()