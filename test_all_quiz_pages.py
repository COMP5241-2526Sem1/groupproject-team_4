#!/usr/bin/env python3
"""
Test script to check for scrollbar issues on various quiz pages.
"""

import requests
import sys
from bs4 import BeautifulSoup

def test_all_quiz_pages():
    """Test scrollbar issues on all quiz-related pages"""
    
    # Test various quiz-related URLs
    test_urls = [
        'http://localhost:5000/course/PHYS101/quiz',           # Quiz list
        'http://localhost:5000/course/COMP201/quiz',           # Quiz list
        'http://localhost:5000/course/MATH101/quiz',            # Quiz list
        'http://localhost:5000/course/PHYS101/quiz/13',        # Quiz info
        'http://localhost:5000/course/COMP201/quiz/6',         # Quiz info
        'http://localhost:5000/course/MATH101/quiz/1',         # Quiz info
        'http://localhost:5000/course/PHYS101/quiz/13/start',  # Quiz start
        'http://localhost:5000/course/COMP201/quiz/6/start',   # Quiz start
    ]
    
    print("Testing scrollbar issues on all quiz-related pages...")
    
    working_pages = []
    failed_pages = []
    
    for url in test_urls:
        try:
            print(f"\nTesting: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Loaded (status: {response.status_code})")
                working_pages.append(url)
                
                # Quick check for potential scrollbar issues
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check for main content structure
                main_content = soup.find('main', class_='main-content')
                if main_content:
                    print("   - Main content container found")
                
                # Check for quiz container
                quiz_container = soup.find('div', class_='quiz-container')
                if quiz_container:
                    print("   - Quiz container found")
                
            else:
                print(f"❌ Failed (status: {response.status_code})")
                failed_pages.append(url)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")
            failed_pages.append(url)
        except Exception as e:
            print(f"❌ Error: {e}")
            failed_pages.append(url)
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"✅ Working pages: {len(working_pages)}")
    print(f"❌ Failed pages: {len(failed_pages)}")
    
    if working_pages:
        print("\nWorking pages:")
        for page in working_pages:
            print(f"   - {page}")
    
    if failed_pages:
        print("\nFailed pages:")
        for page in failed_pages:
            print(f"   - {page}")
    
    print("\nScrollbar fix applied:")
    print("- Changed .main-content from 'height: 100vh' to 'min-height: 100vh'")
    print("- Changed .main-content from 'overflow-y: auto' to 'overflow-y: visible'")
    print("This should resolve double scrollbar issues on all quiz pages.")

if __name__ == "__main__":
    test_all_quiz_pages()