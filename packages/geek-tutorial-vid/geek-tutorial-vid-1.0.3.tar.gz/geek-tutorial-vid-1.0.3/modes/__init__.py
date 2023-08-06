import cloudscraper

def credits():
    scraper = cloudscraper.create_scraper()
    return scraper.get("https://geekis.dev/").json()['skidder']