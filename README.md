# ScrapEarn - Business Lead Scraper

Scrape business leads from JustDial and IndiaMart for custom software development services.

## Setup

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Chrome browser (required for Selenium)

## Usage

Run the scraper:
```bash
python scraper.py
```

Results will be saved to `custom_software_leads_uttar_pradesh.csv`

## Customization

Edit `scraper.py` to modify:
- `KEYWORDS`: Target industries/services
- `LOCATIONS`: Geographic regions
- `max_pages`: Number of pages to scrape per search
