# tools.py
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def search_anime_web(query: str) -> str:
    """Searches the internet for anime data and extracts relevant context paragraphs."""
    search_url = f"https://duckduckgo.com{query}+anime+fandom+wiki"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', class_='result__url')]
        
        if links:
            target_page = requests.get(f"https:{links}", headers=headers, timeout=8)
            page_soup = BeautifulSoup(target_page.text, 'html.parser')
            paragraphs = page_soup.find_all('p')
            text_data = "\n".join([pget_text() for p in paragraphs[:]])
            return text_data if text_data.strip() else "No lore content found."
    except Exception as e:
        return f"Extraction trace failed: {str(e)}"
        
    return "No database records found online."
