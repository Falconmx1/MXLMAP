import sys
import time

def banner():
    with open('banners/banner_mx.txt', 'r', encoding='utf-8') as f:
        print(f.read())
    time.sleep(1)

def print_status(message, status_type="INFO"):
    colors = {
        "INFO": "\033[94m[*]\033[0m",
        "SUCCESS": "\033[92m[+]\033[0m",
        "ERROR": "\033[91m[-]\033[0m",
        "WARNING": "\033[93m[!]\033[0m"
    }
    print(f"{colors.get(status_type, '[?]')} {message}")
