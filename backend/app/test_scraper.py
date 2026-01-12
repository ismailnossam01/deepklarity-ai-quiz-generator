"""
Test script to debug Wikipedia scraping
Run this to see what's being extracted
"""

import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Alan_Turing"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching: {url}")
response = requests.get(url, headers=headers, timeout=15)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)} bytes")

# Save HTML to file for inspection
with open("debug_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)
print("✅ Saved HTML to debug_page.html")

# Parse
soup = BeautifulSoup(response.text, 'html.parser')

# Try to find content divs
print("\n" + "="*60)
print("Testing different selectors:")
print("="*60)

# Test 1
div1 = soup.find('div', {'class': 'mw-parser-output'})
print(f"1. div class='mw-parser-output': {'FOUND' if div1 else 'NOT FOUND'}")
if div1:
    paragraphs = div1.find_all('p')
    print(f"   Paragraphs found: {len(paragraphs)}")
    if paragraphs:
        print(f"   First paragraph text: {paragraphs[0].get_text()[:100]}...")

# Test 2
div2 = soup.find('div', {'id': 'mw-content-text'})
print(f"2. div id='mw-content-text': {'FOUND' if div2 else 'NOT FOUND'}")
if div2:
    paragraphs = div2.find_all('p')
    print(f"   Paragraphs found: {len(paragraphs)}")

# Test 3
div3 = soup.find('div', {'id': 'bodyContent'})
print(f"3. div id='bodyContent': {'FOUND' if div3 else 'NOT FOUND'}")

# Test 4 - Get ALL paragraphs
all_p = soup.find_all('p')
print(f"4. ALL paragraphs in page: {len(all_p)}")
if all_p:
    for i, p in enumerate(all_p[:5]):
        text = p.get_text().strip()
        if text:
            print(f"   P{i}: {text[:80]}...")

print("\n" + "="*60)
print("Run this script with: python test_scraper.py")
print("Check debug_page.html to see the actual HTML structure")
print("="*60)