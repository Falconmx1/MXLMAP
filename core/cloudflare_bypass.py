import requests
import time
import random
from bs4 import BeautifulSoup

class CloudflareBypass:
    def __init__(self, session):
        self.session = session
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
    
    def detect_and_bypass(self, url):
        """Detecta y evade Cloudflare automáticamente"""
        print("[CF] Detectando Cloudflare...")
        
        # Detectar Cloudflare
        try:
            response = self.session.get(url, timeout=10)
            if 'cf-ray' in response.headers or 'cloudflare' in response.text.lower():
                print("[CF] Cloudflare detectado! Iniciando bypass...")
                return self.bypass_cloudflare(url)
            return response
        except:
            return None
    
    def bypass_cloudflare(self, url):
        """Múltiples técnicas para bypass CF"""
        techniques = [
            self.use_cloudscraper,
            self.rotate_headers,
            self.use_tor_rotation,
            self.emulate_browser
        ]
        
        for technique in techniques:
            result = technique(url)
            if result and 'cf-ray' not in result.headers:
                print(f"[CF] Bypass exitoso con: {technique.__name__}")
                return result
        return None
    
    def use_cloudscraper(self, url):
        """Usa cloudscraper para resolver challenges"""
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper()
            return scraper.get(url)
        except:
            return None
    
    def rotate_headers(self, url):
        """Rota headers para evitar detección"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        return self.session.get(url, headers=headers)
    
    def use_tor_rotation(self, url):
        """Rota IPs via Tor"""
        session = requests.Session()
        session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        return session.get(url, timeout=15)
    
    def emulate_browser(self, url):
        """Emula comportamiento real de navegador"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.user_agents[0],
            'Accept-Language': 'es-MX,es;q=0.9',
        })
        
        # Descarga recursos como un browser real
        session.get(url)
        time.sleep(random.uniform(1, 3))
        return session.get(url)
