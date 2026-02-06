import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

# Anti-detection headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# Target keywords for custom software leads
KEYWORDS = ['custom software', 'software development', 'web developer', 'app developer', 'crm software', 'website developer']
LOCATIONS = ['Noida', 'Dadri', 'Greater Noida', 'Uttar Pradesh']

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=" + HEADERS['User-Agent'])
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_justdial(driver, keyword, location, max_pages=3):
    """Scrape JustDial for business leads needing software services"""
    results = []
    base_url = f"https://www.justdial.com/{location}/{keyword}/nct-10000000"
    
    for page in range(1, max_pages + 1):
        try:
            url = f"{base_url}/page-{page}" if page > 1 else base_url
            driver.get(url)
            time.sleep(random.uniform(2, 4))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            listings = soup.find_all('div', class_='store-details') or soup.find_all('li', class_='cntanr')
            
            for listing in listings[:10]:  # Top 10 per page
                try:
                    name = listing.find('h2') or listing.find('a', class_='lngrfl')
                    name = name.text.strip() if name else 'N/A'
                    
                    phone = listing.find('span', class_='contact-info') or listing.find('a', {'data-clk': 'tel'})
                    phone = phone.text.strip() if phone else 'N/A'
                    
                    address = listing.find('span', class_='address') or listing.find('div', class_='adrstxt')
                    address = address.text.strip() if address else 'N/A'
                    
                    # Score for custom software intent
                    intent_score = 8 if any(kw in name.lower() for kw in KEYWORDS) else 5
                    
                    results.append({
                        'platform': 'JustDial',
                        'business_name': name,
                        'phone': phone,
                        'address': address,
                        'keyword': keyword,
                        'location': location,
                        'intent_score': intent_score,
                        'url': driver.current_url
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"Page {page} error: {e}")
            continue
    
    return results

def scrape_indiamart_requests():
    """Scrape IndiaMart inquiry/RFP section for custom software needs"""
    results = []
    # IndiaMart buyer inquiries (manual search recommended: indiamart.com > Post Buy Requirement)
    urls = [
        'https://m.indiamart.com/inquiry/software-development-services/',
        'https://dir.indiamart.com/noida/software-development-service.html'
    ]
    
    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            inquiries = soup.find_all('div', class_='inquiry-box') or soup.find_all('div', {'data-qid': True})
            for inquiry in inquiries[:20]:
                title = inquiry.find('a', class_='inquiry-title')
                title = title.text.strip() if title else 'N/A'
                
                if any(kw in title.lower() for kw in KEYWORDS):
                    results.append({
                        'platform': 'IndiaMart',
                        'inquiry_title': title,
                        'url': url,
                        'intent_score': 10  # High intent from buyer inquiries
                    })
        except:
            continue
    
    return results

def main():
    driver = setup_driver()
    all_leads = []
    
    print("🕷️ Scraping JustDial for custom software leads...")
    for loc in LOCATIONS:
        for kw in KEYWORDS:
            print(f"Searching {kw} in {loc}...")
            leads = scrape_justdial(driver, kw.replace(' ', '-'), loc, max_pages=2)
            all_leads.extend(leads)
            time.sleep(3)
    
    print("📱 Scraping IndiaMart inquiries...")
    all_leads.extend(scrape_indiamart_requests())
    
    driver.quit()
    
    # Deduplicate and filter high-intent leads
    df = pd.DataFrame(all_leads)
    df.drop_duplicates(subset=['business_name', 'phone'], inplace=True)
    high_intent = df[df['intent_score'] >= 7].sort_values('intent_score', ascending=False)
    
    # Export
    high_intent.to_csv('custom_software_leads_uttar_pradesh.csv', index=False)
    print(f"✅ Exported {len(high_intent)} high-intent leads to CSV!")
    
    # Show top 10
    print("\n🎯 TOP 10 HOTTEST LEADS:")
    for _, lead in high_intent.head(10).iterrows():
        print(f"📞 {lead['phone']} | {lead['business_name'][:50]}... | Score: {lead['intent_score']}")

if __name__ == "__main__":
    main()
