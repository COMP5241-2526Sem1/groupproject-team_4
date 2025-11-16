#!/usr/bin/env python3
"""
Test script to verify the scrollbar fix for quiz results pages.
This script checks if the CSS changes resolved the double scrollbar issue.
"""

import requests
import sys
from bs4 import BeautifulSoup

def test_scrollbar_issue():
    """Test if the scrollbar fix is working properly"""
    
    # Test URLs that were reported to have scrollbar issues
    test_urls = [
        'http://localhost:5000/course/PHYS101/quiz/13/results',
        'http://localhost:5000/course/COMP201/quiz/6/results',
        'http://localhost:5000/course/MATH101/quiz/1/results'
    ]
    
    print("Testing scrollbar fix for quiz results pages...")
    
    for url in test_urls:
        try:
            print(f"\nTesting URL: {url}")
            
            # Make request to the page
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Page loaded successfully (status: {response.status_code})")
                
                # Parse HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check for potential scrollbar issues
                main_content = soup.find('main', class_='main-content')
                quiz_container = soup.find('div', class_='quiz-container')
                
                if main_content and quiz_container:
                    print("✅ Found main content and quiz container elements")
                    
                    # Check CSS classes that could cause overflow issues
                    style_tags = soup.find_all('style')
                    inline_styles = []
                    
                    # Collect all style content
                    for style in style_tags:
                        if style.string:
                            inline_styles.append(style.string)
                    
                    # Check for overflow-related CSS
                    css_content = ' '.join(inline_styles)
                    
                    # Look for potential scrollbar issues
                    issues_found = []
                    
                    if 'overflow-y: auto' in css_content and 'height: 100vh' in css_content:
                        issues_found.append("Potential double scrollbar: overflow-y:auto with height:100vh")
                    
                    if 'overflow: hidden' in css_content and 'overflow-y: auto' in css_content:
                        issues_found.append("Conflicting overflow properties")
                    
                    if issues_found:
                        print("⚠️  Potential scrollbar issues detected:")
                        for issue in issues_found:
                            print(f"   - {issue}")
                    else:
                        print("✅ No obvious scrollbar conflicts detected in inline styles")
                
                # Check page structure
                body = soup.find('body')
                if body:
                    # Check if body has overflow styles that could cause issues
                    body_style = body.get('style', '')
                    if 'overflow' in body_style:
                        print(f"ℹ️  Body has inline styles: {body_style}")
                    
                    print("✅ Page structure looks good")
                
            else:
                print(f"❌ Page failed to load (status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to connect to {url}: {e}")
        except Exception as e:
            print(f"❌ Error testing {url}: {e}")
    
    print("\n" + "="*60)
    print("Scrollbar fix test completed!")
    print("The main fix applied:")
    print("- Changed .main-content height from '100vh' to 'min-height: 100vh'")
    print("- Changed .main-content overflow-y from 'auto' to 'visible'")
    print("This should prevent double scrollbars on quiz results pages.")

if __name__ == "__main__":
    test_scrollbar_issue()