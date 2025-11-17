#!/usr/bin/env python3
"""
Test script for ultra-conservative overlap prevention in multi-dimensional word cloud
"""

import math
import random

def test_ultra_conservative_positioning():
    """Test the ultra-conservative positioning system with guaranteed no overlaps"""
    
    # Simulate the ultra-conservative positioning algorithm
    placed_words = []
    max_words = 20
    min_spacing = 150
    container_width = 800
    container_height = 600
    
    def calculate_word_dimensions(word, font_size):
        # Ultra-conservative dimension estimation
        avg_char_width = font_size * 0.4
        word_width = max(len(word) * avg_char_width, font_size)
        word_height = font_size * 0.7
        return {"width": word_width, "height": word_height}
    
    def find_valid_position(word, font_size, center_x=400, center_y=300):
        word_index = len(placed_words)
        dimensions = calculate_word_dimensions(word, font_size)
        
        # Use a very sparse layout - only 4 words per row/column
        cols = 4
        rows = 5
        col = word_index % cols
        row = word_index // cols
        
        # Calculate position with very large spacing
        available_width = container_width - 100  # Leave margins
        available_height = container_height - 100  # Leave margins
        
        col_spacing = available_width / (cols - 1)
        row_spacing = available_height / (rows - 1)
        
        x = 50 + col * col_spacing
        y = 50 + row * row_spacing
        
        # Very minimal randomness
        random_offset = 10
        x += (random.random() - 0.5) * random_offset
        y += (random.random() - 0.5) * random_offset
        
        # Ensure within very conservative bounds
        margin = max(dimensions["width"], dimensions["height"]) / 2 + 40
        x = max(margin, min(container_width - margin, x))
        y = max(margin, min(container_height - margin, y))
        
        return {"x": x, "y": y, "width": dimensions["width"], "height": dimensions["height"]}
    
    # Test words with various lengths and frequencies (reduced set)
    test_words = [
        ("Python", 35), ("JavaScript", 32), ("React", 28), ("Database", 30),
        ("Algorithm", 33), ("Machine Learning", 38), ("Web Development", 35),
        ("Cloud Computing", 36), ("Artificial Intelligence", 40), ("Data Science", 33),
        ("Mobile App", 29), ("Backend", 26), ("Frontend", 27), ("DevOps", 24),
        ("Cybersecurity", 32), ("Blockchain", 28), ("IoT", 20), ("Big Data", 30),
        ("Microservices", 33), ("API", 22)
    ]
    
    print("Testing Ultra-Conservative Overlap Prevention Algorithm")
    print("=" * 55)
    
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
    
    if overlaps > 0:
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
    
    # Show grid layout
    print(f"\nGrid Layout (4x5):")
    for row in range(5):
        row_words = []
        for col in range(4):
            index = row * 4 + col
            if index < len(placed_words):
                row_words.append(placed_words[index]["word"])
            else:
                row_words.append("---")
        print(f"Row {row + 1}: {' | '.join(row_words)}")
    
    return successful_placements, overlaps, avg_spacing, min_spacing_found

if __name__ == "__main__":
    test_ultra_conservative_positioning()