#!/usr/bin/env python3
"""Test to verify that AI-generated polls conform to poll format specification"""

from llm import generate_poll_content
import json

# Test poll generation
print("Testing poll generation...")
print("-" * 50)

try:
    poll_data = generate_poll_content("DNS services", "", 3)
    
    print("✓ Poll generated successfully!")
    print("\nGenerated Poll Structure:")
    print(json.dumps(poll_data, indent=2, ensure_ascii=False))
    
    # Validation checks
    print("\n" + "=" * 50)
    print("Validation Checks:")
    print("=" * 50)
    
    # Check required fields
    required_fields = ['poll_name', 'description', 'duration', 'questions']
    for field in required_fields:
        if field in poll_data:
            print(f"✓ {field}: Present")
        else:
            print(f"✗ {field}: Missing")
    
    # Check questions structure
    if 'questions' in poll_data:
        questions = poll_data['questions']
        print(f"\n✓ Number of questions: {len(questions)}")
        
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}:")
            print(f"  - type: {q.get('type')} (should be 'mcq' for polls)")
            print(f"  - content: {q.get('content')[:50]}...")
            print(f"  - points: {q.get('points')} (should be 0 for polls)")
            
            # Check choices
            if 'choices' in q:
                print(f"  - choices count: {len(q['choices'])}")
                for j, choice in enumerate(q['choices'], 1):
                    correct = choice.get('correct')
                    print(f"    {chr(64+j)}. {choice.get('text')[:30]}... (correct: {correct})")
                    
                    # Poll format requirement: all choices should have correct=false
                    if correct != False:
                        print(f"       ⚠️ WARNING: In polls, all choices should have correct=false!")
    
    print("\n" + "=" * 50)
    print("Format Compliance Summary:")
    print("=" * 50)
    
    # Check poll format compliance
    compliant = True
    
    # All questions should be MCQ
    all_mcq = all(q.get('type') == 'mcq' for q in poll_data.get('questions', []))
    print(f"{'✓' if all_mcq else '✗'} All questions are MCQ type")
    if not all_mcq:
        compliant = False
    
    # All questions should have points=0
    all_zero_points = all(q.get('points') == 0 for q in poll_data.get('questions', []))
    print(f"{'✓' if all_zero_points else '✗'} All questions have points=0")
    if not all_zero_points:
        compliant = False
    
    # All choices should have correct=false
    all_false_correct = all(
        c.get('correct') == False 
        for q in poll_data.get('questions', []) 
        for c in q.get('choices', [])
    )
    print(f"{'✓' if all_false_correct else '✗'} All choices have correct=false")
    if not all_false_correct:
        compliant = False
    
    # Has required fields
    has_required = all(f in poll_data for f in required_fields)
    print(f"{'✓' if has_required else '✗'} Has all required fields")
    if not has_required:
        compliant = False
    
    print("\n" + "=" * 50)
    if compliant:
        print("✓ Poll format is COMPLIANT with specification!")
    else:
        print("✗ Poll format has ISSUES - see warnings above")
    print("=" * 50)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
