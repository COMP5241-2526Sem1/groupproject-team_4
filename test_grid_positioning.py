#!/usr/bin/env python3
"""
Test script for grid-based overlap prevention in multi-dimensional word cloud
"""

import math
import random

def test_grid_positioning():
    """Test the grid-based positioning system with guaranteed spacing"""
    
    # Simulate the grid-based positioning algorithm
    placed_words = []
    max_words = 30
    grid_spacing = 120
    container_width = 800
    container_height = 600
    
    def calculate_word_dimensions(word, font_size):
        # Very conservative dimension estimation
        avg_char_width = font_size * 0.45
        word_width = max(len(word) * avg_char_width, font_size * 1.2)
        word_height = font_size * 0.8
        return {"width": word_width, "height": word_height}
    
    def find_valid_position(word, font_size, center_x=400, center_y=300):
        word_index = len(placed_words)
        dimensions = calculate_word_dimensions(word, font_size)
        
        # Simple grid-based positioning with guaranteed spacing
        cols = 6  # 6 columns in the grid
        rows = 5  # 5 rows in the grid
        col = word_index % cols
        row = word_index // cols
        
        # Calculate position with large spacing
        start_x = (container_width - (cols - 1) * grid_spacing) / 2
        start_y = (container_height - (rows - 1) * grid_spacing) / 2
        
        x = start_x + col * grid_spacing
        y = start_y + row * grid_spacing
        
        # Add some randomness to avoid perfect alignment
        random_offset = 20
        x += (random.random() - 0.5) * random_offset
        y += (random.random() - 0.5) * random_offset
        
        # Ensure within bounds
        margin = max(dimensions["width"], dimensions["height"]) / 2 + 30
        x = max(margin, min(container_width - margin, x))
        y = max(margin, min(container_height - margin, y))
        
        return {"x": x, "y": y, "width": dimensions["width"], "height": dimensions["height"]}
    
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
    
    print("Testing Grid-Based Overlap Prevention Algorithm")
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
    
    # Verify grid spacing
    expected_min_spacing = grid_spacing - 40  # Account for random offset
    actual_min_spacing = float('inf')
    
    for i, word1 in enumerate(placed_words):
        for j, word2 in enumerate(placed_words):
            if i != j:
                distance = math.sqrt((word1["x"] - word2["x"])**2 + (word1["y"] - word2["y"])**2)
                actual_min_spacing = min(actual_min_spacing, distance)
    
    print(f"Expected minimum spacing: {expected_min_spacing}px")
    print(f"Actual minimum spacing: {actual_min_spacing:.1f}px")
    
    # Show grid layout
    print(f"\nGrid Layout:")
    for row in range(5):
        row_words = []
        for col in range(6):
            index = row * 6 + col
            if index < len(placed_words):
                row_words.append(placed_words[index]["word"])
            else:
                row_words.append("---")
        print(f"Row {row + 1}: {' | '.join(row_words)}")
    
    return successful_placements, overlaps, actual_min_spacing

if __name__ == "__main__":
    test_grid_positioning()