"""
Wikipedia article scraper using BeautifulSoup.
Extracts content, sections, and entities from Wikipedia pages.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re

class WikipediaScraper:
    """Scrapes and extracts information from Wikipedia articles."""
    
    def __init__(self):
        """Initialize the scraper with headers to mimic a browser."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def is_valid_wikipedia_url(self, url: str) -> bool:
        """Check if URL is a valid Wikipedia article URL."""
        pattern = r'https?://(en\.)?wikipedia\.org/wiki/.+'
        return bool(re.match(pattern, url))
    
    def scrape_article(self, url: str) -> Dict:
        """
        Main function to scrape a Wikipedia article.
        Returns a dictionary with all extracted information.
        """
        # Validate URL
        if not self.is_valid_wikipedia_url(url):
            raise ValueError("Invalid Wikipedia URL. Must be like: https://en.wikipedia.org/wiki/Article_Name")
        
        print(f"   🌐 Fetching URL: {url}")
        
        # Fetch the page
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            print(f"   ✅ Got response: {response.status_code}")
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch Wikipedia page: {str(e)}")
        
        # Parse HTML - try html.parser (most reliable)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all information
        title = self._extract_title(soup)
        content = self._extract_content(soup)
        
        print(f"   📄 Title: {title}")
        print(f"   📝 Content length: {len(content)} characters")
        
        if not content or len(content) < 100:
            print(f"   ⚠️  WARNING: Very short content extracted!")
        
        return {
            'url': url,
            'title': title,
            'summary': self._extract_summary(soup),
            'content': content,
            'sections': self._extract_sections(soup),
            'key_entities': self._extract_entities(soup),
            'raw_html': None  # Don't store raw HTML to save space
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title."""
        # Try multiple selectors
        title_tag = soup.find('h1', class_='firstHeading')
        if not title_tag:
            title_tag = soup.find('h1', id='firstHeading')
        if not title_tag:
            title_tag = soup.find('title')
            if title_tag:
                # Remove " - Wikipedia" from title
                return title_tag.get_text().replace(' - Wikipedia', '').strip()
        
        return title_tag.get_text().strip() if title_tag else "Unknown Title"
    
    def _extract_summary(self, soup: BeautifulSoup) -> str:
        """Extract first paragraph as summary."""
        # Find all paragraphs in main content
        content = soup.find('div', class_='mw-parser-output')
        if not content:
            content = soup.find('div', id='mw-content-text')
        
        if not content:
            return ""
        
        # Get first substantial paragraph
        paragraphs = content.find_all('p', recursive=False)
        for p in paragraphs:
            text = p.get_text().strip()
            # Skip very short paragraphs and coordinates
            if len(text) > 100 and not text.startswith('Coordinates:'):
                # Clean up
                text = re.sub(r'\[\d+\]', '', text)  # Remove citations
                return text[:500]  # Return first 500 chars
        
        return ""
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content (for LLM processing)."""
        # Try multiple strategies to find content
        content = None
        
        # Strategy 1: Find by id mw-content-text (THIS WORKS!)
        content = soup.find('div', {'id': 'mw-content-text'})
        if not content:
            # Strategy 2: Find mw-parser-output
            content = soup.find('div', {'class': 'mw-parser-output'})
        if not content:
            # Strategy 3: Find by id bodyContent
            content = soup.find('div', {'id': 'bodyContent'})
        
        if not content:
            print("   ⚠️  Could not find main content div")
            return ""
        
        # Get ALL paragraphs (not just direct children)
        paragraphs = content.find_all('p')
        
        if not paragraphs:
            print("   ⚠️  No paragraphs found")
            # Try to get any text
            text = content.get_text()
            print(f"   📝 Extracted raw text: {len(text)} characters")
            if len(text) > 500:
                # Clean and return
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:8000]
            return ""
        
        print(f"   📊 Found {len(paragraphs)} paragraphs total")
        
        # Collect text from substantial paragraphs
        text_parts = []
        for i, p in enumerate(paragraphs):
            text = p.get_text().strip()
            
            # Skip empty paragraphs
            if not text:
                continue
            
            # Skip very short paragraphs (likely metadata)
            if len(text) < 20:
                continue
                
            # Skip coordinate paragraphs
            if text.startswith('Coordinates:'):
                continue
            
            # Add to collection
            text_parts.append(text)
            
            # Collect enough for good quiz (stop after ~20 paragraphs or 6000 chars)
            if len(text_parts) >= 20 or sum(len(t) for t in text_parts) > 6000:
                break
        
        if not text_parts:
            print("   ⚠️  No text extracted from paragraphs")
            return ""
        
        print(f"   ✅ Collected text from {len(text_parts)} paragraphs")
        
        # Join paragraphs
        full_text = ' '.join(text_parts)
        
        # Clean up text
        full_text = re.sub(r'\[\d+\]', '', full_text)  # Remove citation numbers
        full_text = re.sub(r'\s+', ' ', full_text)     # Normalize whitespace
        full_text = full_text.strip()
        
        # Limit to 8000 characters for LLM
        if len(full_text) > 8000:
            full_text = full_text[:8000]
        
        print(f"   ✅ Final content: {len(full_text)} characters")
        
        return full_text
    
    def _extract_sections(self, soup: BeautifulSoup) -> List[str]:
        """Extract section headings from the article."""
        sections = []
        
        # Find all h2 and h3 headings
        headings = soup.find_all(['h2', 'h3'])
        
        for heading in headings:
            # Get the headline span
            headline = heading.find('span', class_='mw-headline')
            if headline:
                section_text = headline.get_text().strip()
                # Skip common navigation sections
                skip_sections = ['Contents', 'References', 'External links', 'See also', 'Notes', 'Bibliography']
                if section_text not in skip_sections:
                    sections.append(section_text)
        
        return sections[:10]  # Return first 10 sections
    
    def _extract_entities(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """
        Extract named entities (people, organizations, locations).
        Uses simple heuristics based on Wikipedia links.
        """
        entities = {
            'people': [],
            'organizations': [],
            'locations': []
        }
        
        # Find main content
        content = soup.find('div', class_='mw-parser-output')
        if not content:
            return entities
        
        # Find all internal Wikipedia links
        links = content.find_all('a', href=re.compile(r'^/wiki/'))
        
        seen = set()
        for link in links[:100]:  # Check first 100 links
            text = link.get_text().strip()
            href = link.get('href', '')
            
            # Skip if text is too short or is a date/year
            if len(text) < 3 or text.isdigit() or len(text) > 50:
                continue
            
            # Skip common Wikipedia pages
            if any(skip in href for skip in ['Wikipedia:', 'Help:', 'Category:', 'File:', 'Template:', 'Portal:']):
                continue
            
            # Skip if already seen
            if text in seen:
                continue
            seen.add(text)
            
            # Simple categorization based on text patterns
            if any(word in text for word in ['University', 'Institute', 'Company', 'Organization', 'Corporation', 'Association']):
                if len(entities['organizations']) < 5:
                    entities['organizations'].append(text)
            elif any(word in text for word in ['United States', 'Kingdom', 'City', 'Country', 'State']):
                if len(entities['locations']) < 5:
                    entities['locations'].append(text)
            else:
                # Check if it looks like a person name (2-4 capitalized words)
                words = text.split()
                if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                    if len(entities['people']) < 5:
                        entities['people'].append(text)
        
        return entities