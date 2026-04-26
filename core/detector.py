import requests

class SQLDetector:
    def __init__(self, url):
        self.url = url
        self.payloads = ["'", "\"", "1' OR '1'='1", "1' AND '1'='2"]
        
    def check_vulnerability(self):
        print("Probando payloads básicos...")
        for payload in self.payloads:
            test_url = self.url + payload
            try:
                response = requests.get(test_url, timeout=5)
                if self.is_vulnerable(response):
                    return True
            except:
                continue
        return False
    
    def is_vulnerable(self, response):
        error_signs = ["mysql", "sql syntax", "microsoft ole db", "oracle", "postgresql"]
        return any(sign in response.text.lower() for sign in error_signs)
