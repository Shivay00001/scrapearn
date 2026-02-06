import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

KEYWORDS = ['custom software development', 'software company', 'web development company', 'app development services', 'CRM software development']
LOCATIONS = ['Noida', 'Greater Noida']

def scrape_google_maps_results(keyword, location):
    results = []
    query = f"{keyword} in {location}"
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/maps/search/{encoded_query}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            scripts = soup.find_all('script')
            for script in scripts:
                if 'business' in script.text.lower() or 'name' in script.text.lower():
                    try:
                        import re
                        pattern = r'\["([^"]+)"\]'
                        matches = re.findall(pattern, script.text)
                        if len(matches) > 3:
                            name = matches[0] if matches[0] else 'N/A'
                            results.append({
                                'platform': 'Google Maps',
                                'business_name': name[:50],
                                'phone': 'N/A',
                                'address': location,
                                'keyword': keyword,
                                'location': location,
                                'intent_score': 7,
                                'url': url
                            })
                            if len(results) >= 5:
                                break
                    except:
                        continue
    except Exception as e:
        print(f"  Error: {e}")
    
    return results

def scrape_google_search(keyword, location):
    results = []
    query = f"{keyword} in {location} contact"
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            divs = soup.find_all('div', {'data-ved': True})[:10]
            for div in divs:
                try:
                    a_tag = div.find('a')
                    if a_tag:
                        name = a_tag.text.strip()
                        link = a_tag.get('href', '')
                        if name and 'http' not in name and len(name) > 5:
                            results.append({
                                'platform': 'Google Search',
                                'business_name': name[:50],
                                'phone': 'N/A',
                                'address': location,
                                'keyword': keyword,
                                'location': location,
                                'intent_score': 6,
                                'url': link
                            })
                            if len(results) >= 5:
                                break
                except:
                    continue
    except Exception as e:
        print(f"  Error: {e}")
    
    return results

def generate_mock_leads():
    """Generate sample leads for demonstration"""
    sample_businesses = [
        {'name': 'TechSolutions India Pvt Ltd', 'phone': '+91-9876543210', 'address': 'Sector 62, Noida'},
        {'name': 'Digital Web Developers', 'phone': '+91-9876543211', 'address': 'Sector 63, Noida'},
        {'name': 'AppCraft Software', 'phone': '+91-9876543212', 'address': 'Greater Noida West'},
        {'name': 'CodeBridge Technologies', 'phone': '+91-9876543213', 'address': 'Sector 16, Noida'},
        {'name': 'NextGen CRM Solutions', 'phone': '+91-9876543214', 'address': 'Sector 18, Noida'},
        {'name': 'WebWizard Studios', 'phone': '+91-9876543215', 'address': 'Greater Noida'},
        {'name': 'SoftServe India', 'phone': '+91-9876543216', 'address': 'Sector 5, Noida'},
        {'name': 'DataDriven CRM', 'phone': '+91-9876543217', 'address': 'Sector 125, Noida'},
        {'name': 'AppMinds Technology', 'phone': '+91-9876543218', 'address': 'Greater Noida'},
        {'name': 'CustomCode Labs', 'phone': '+91-9876543219', 'address': 'Sector 62, Noida'},
    ]
    
    results = []
    for i, biz in enumerate(sample_businesses):
        results.append({
            'platform': 'Sample Data',
            'business_name': biz['name'],
            'phone': biz['phone'],
            'address': biz['address'],
            'keyword': KEYWORDS[i % len(KEYWORDS)],
            'location': biz['address'].split(', ')[-1] if ',' in biz['address'] else LOCATIONS[i % len(LOCATIONS)],
            'intent_score': random.randint(5, 10),
            'url': 'https://example.com'
        })
    
    return results

def main():
    all_leads = []
    
    print("Generating sample leads for demonstration...")
    all_leads = generate_mock_leads()
    
    print("\nAttempting web scraping (may be limited by anti-bot measures)...")
    for loc in LOCATIONS[:1]:
        for kw in KEYWORDS[:2]:
            print(f"Searching {kw} in {loc}...")
            google_leads = scrape_google_search(kw, loc)
            all_leads.extend(google_leads)
            time.sleep(2)
    
    if all_leads:
        df = pd.DataFrame(all_leads)
        df.drop_duplicates(subset=['business_name', 'phone'], inplace=True)
        high_intent = df.sort_values('intent_score', ascending=False)
        
        high_intent.to_csv('custom_software_leads_uttar_pradesh.csv', index=False)
        print(f"\nExported {len(high_intent)} leads to CSV!")
        
        print("\nTOP 10 LEADS:")
        for idx, (_, lead) in enumerate(high_intent.head(10).iterrows(), 1):
            print(f"{idx}. {lead['business_name']} | {lead['phone']} | {lead['location']} | Score: {lead['intent_score']}")
    else:
        print("No leads found.")

if __name__ == "__main__":
    main()
