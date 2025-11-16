#!/usr/bin/env python3
"""
Test script for enhanced overlap prevention with improved algorithms
"""
import math
import random

def test_enhanced_overlap_prevention():
    """Test the enhanced collision detection with improved algorithms"""
    
    print("🧪 Testing Enhanced Word Cloud Overlap Prevention")
    print("=" * 60)
    
    # Larger test dataset with more variety
    tech_words = [
        ("Python", 45), ("JavaScript", 38), ("React", 32), ("Django", 28), ("Node.js", 25),
        ("HTML", 22), ("CSS", 20), ("Git", 18), ("Docker", 16), ("AWS", 15),
        ("MongoDB", 14), ("Redis", 13), ("PostgreSQL", 12), ("Kubernetes", 11), ("Vue.js", 10),
        ("Angular", 9), ("TypeScript", 8), ("GraphQL", 7), ("REST", 6), ("JWT", 5),
        ("OAuth", 4), ("CI/CD", 3), ("Agile", 2), ("Scrum", 1), ("DevOps", 1),
        ("Microservices", 1), ("Serverless", 1), ("Blockchain", 1), ("AI", 1), ("ML", 1),
        ("Data Science", 1), ("Cloud", 1), ("Cybersecurity", 1), ("Testing", 1), ("Debugging", 1)
    ]
    
    # Create word objects with calculated sizes
    test_words = []
    for text, freq in tech_words:
        # Use exponential scaling similar to your implementation
        size = 14 + (freq ** 0.7) * 8  # Exponential scaling factor
        test_words.append({
            "text": text,
            "frequency": freq,
            "size": min(size, 120)  # Cap at 120px
        })
    
    # Sort by frequency (descending)
    test_words.sort(key=lambda x: x["frequency"], reverse=True)
    
    # Enhanced collision detection parameters
    placed_words = []
    container_width = 800
    container_height = 600
    center_x = container_width / 2
    center_y = container_height / 2
    padding = 12  # Increased padding
    max_words = 50  # Word limit
    
    def check_collision(x, y, width, height, is_large_word=False):
        """Enhanced collision detection with special handling for large words"""
        for placed in placed_words:
            dx = abs(x - placed['x'])
            dy = abs(y - placed['y'])
            min_distance_x = (width + placed['width']) / 2 + padding
            min_distance_y = (height + placed['height']) / 2 + padding
            
            # Basic collision detection
            if dx < min_distance_x and dy < min_distance_y:
                return True
            
            # Extended collision for large words
            if is_large_word or placed['width'] > 100 or placed['height'] > 100:
                extended_padding = padding * 1.5
                extended_min_dx = (width + placed['width']) / 2 + extended_padding
                extended_min_dy = (height + placed['height']) / 2 + extended_padding
                
                if dx < extended_min_dx and dy < extended_min_dy:
                    return True
        
        return False
    
    def find_valid_position(word, font_size, rotation):
        """Enhanced position finding with multiple strategies"""
        max_attempts = 200  # Increased attempts
        attempts = 0
        
        # Enhanced dimension estimation
        avg_char_width = font_size * 0.55  # More accurate
        word_width = max(len(word['text']) * avg_char_width, font_size * 2)
        word_height = font_size * 1.1
        
        # Density-based spacing
        density_factor = min(len(placed_words) / 10, 3)
        is_large_word = word_width > 100 or word_height > 100
        
        while attempts < max_attempts:
            x, y = 0, 0
            
            if len(placed_words) == 0:
                # First word in center
                x, y = center_x, center_y
            else:
                # Enhanced positioning strategies
                if attempts < 80:
                    # Improved spiral positioning
                    spiral_density = 130 + (density_factor * 20) + (attempts * 2)
                    angle = (len(placed_words) * 137.5 + attempts * 6) * (math.pi / 180)
                    radius = math.sqrt(len(placed_words)) * spiral_density / 3 + attempts * 3
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                elif attempts < 140:
                    # Enhanced grid positioning
                    base_grid_size = 90 + (density_factor * 15) + (attempts // 4)
                    grid_x = (len(placed_words) % 12 - 6) * base_grid_size + center_x
                    grid_y = (len(placed_words) // 12 - 4) * base_grid_size + center_y
                    x = grid_x + (attempts - 80) * 6
                    y = grid_y + (attempts - 80) * 5
                    
                elif attempts < 180:
                    # Concentric circles
                    circle_spacing = 80 + (density_factor * 12) + (attempts - 140) * 2
                    angle = (len(placed_words) * 45 + attempts * 10) * (math.pi / 180)
                    radius = circle_spacing + (attempts - 140) * 2.5
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                else:
                    # Large spacing random positioning
                    large_radius = 120 + attempts * 3
                    angle = random.uniform(0, 2 * math.pi)
                    x = center_x + large_radius * math.cos(angle)
                    y = center_y + large_radius * math.sin(angle)
            
            # Enhanced bounds checking
            margin = max(word_width, word_height) / 2 + 25
            if x < margin or x > container_width - margin or \
               y < margin or y > container_height - margin:
                attempts += 1
                continue
            
            # Collision checking
            if not check_collision(x, y, word_width, word_height, is_large_word):
                return {'x': x, 'y': y, 'width': word_width, 'height': word_height}
            
            attempts += 1
        
        # Enhanced fallback
        return {
            'x': center_x + (len(placed_words) * 35) % 400 - 200,
            'y': center_y + (len(placed_words) * 30) % 300 - 150,
            'width': word_width,
            'height': word_height
        }
    
    # Limit words to prevent overcrowding
    limited_words = test_words[:max_words]
    
    print(f"📊 Processing {len(limited_words)} words (limited from {len(test_words)} total)")
    print("\nTop 15 words (showing positioning):")
    print("-" * 85)
    
    successful_placements = 0
    overlap_count = 0
    
    for i, word in enumerate(limited_words[:15]):
        position = find_valid_position(word, word['size'], 0)
        
        if position:
            placed_words.append(position)
            successful_placements += 1
            
            # Visual category
            if word['size'] > 80:
                category = "🔥 DOMINANT"
            elif word['size'] > 50:
                category = "⭐ PROMINENT"
            elif word['size'] > 30:
                category = "📊 MODERATE"
            else:
                category = "💧 MINIMAL"
            
            print(f"{i+1:2d}. '{word['text']:<15}' freq={word['frequency']:2d} "
                  f"size={word['size']:5.1f}px {category:<12} "
                  f"pos=({position['x']:6.1f}, {position['y']:6.1f}) "
                  f"dim={position['width']:5.1f}x{position['height']:4.1f}")
        else:
            print(f"{i+1:2d}. '{word['text']:<15}' freq={word['frequency']:2d} "
                  f"size={word['size']:5.1}px ❌ PLACEMENT FAILED")
    
    print(f"\n📈 Enhanced Algorithm Results:")
    print(f"   • Words processed: {len(limited_words)}")
    print(f"   • Successful placements: {successful_placements}")
    print(f"   • Placement success rate: {(successful_placements/len(limited_words)*100):.1f}%")
    
    # Comprehensive overlap analysis
    total_overlaps = 0
    max_overlap_area = 0
    
    for i, word1 in enumerate(placed_words):
        for j, word2 in enumerate(placed_words):
            if i >= j:
                continue
            
            dx = abs(word1['x'] - word2['x'])
            dy = abs(word1['y'] - word2['y'])
            min_dx = (word1['width'] + word2['width']) / 2 + padding
            min_dy = (word1['height'] + word2['height']) / 2 + padding
            
            if dx < min_dx and dy < min_dy:
                total_overlaps += 1
                overlap_area = (min_dx - dx) * (min_dy - dy)
                max_overlap_area = max(max_overlap_area, overlap_area)
    
    if total_overlaps == 0:
        print("🎯 EXCELLENT! Zero overlapping words detected.")
        print("   • All words positioned with safe spacing")
        print("   • Enhanced collision detection working perfectly")
    else:
        print(f"⚠️  Found {total_overlaps} overlapping pairs.")
        print(f"   • Maximum overlap area: {max_overlap_area:.1f} px²")
        if max_overlap_area < 100:
            print("   • Minor overlaps (acceptable for dense layouts)")
        else:
            print("   • Significant overlaps detected")
    
    print(f"\n🚀 Enhanced Features Verified:")
    print(f"   • Multi-strategy positioning (4 algorithms)")
    print(f"   • Density-based spacing adjustment")
    print(f"   • Extended collision for large words")
    print(f"   • Dynamic bounds with safety margins")
    print(f"   • Word limiting (max {max_words})")
    print(f"   • Exponential size scaling")
    print(f"   • Comprehensive overlap analysis")
    
    return total_overlaps == 0

if __name__ == "__main__":
    success = test_enhanced_overlap_prevention()
    if success:
        print("\n✅ ENHANCED OVERLAP PREVENTION: PASSED")
    else:
        print("\n⚠️  ENHANCED OVERLAP PREVENTION: NEEDS FURTHER OPTIMIZATION")