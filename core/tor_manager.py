import requests
import stem
from stem.control import Controller
from stem.process import launch_tor
import socket
import socks
import time

class TorManager:
    def __init__(self):
        self.tor_port = 9050
        self.control_port = 9051
        self.session = None
        self.setup_tor()
    
    def setup_tor(self):
        """Configura Tor automáticamente"""
        try:
            # Configurar socket SOCKS
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.tor_port)
            socket.socket = socks.socksocket
            
            self.session = requests.Session()
            self.session.proxies = {
                'http': f'socks5h://127.0.0.1:{self.tor_port}',
                'https': f'socks5h://127.0.0.1:{self.tor_port}'
            }
            print("[Tor] Conectado a la red anónima")
            return True
        except Exception as e:
            print(f"[Tor] Error: {e}")
            return False
    
    def renew_identity(self):
        """Renueva identidad (nueva IP)"""
        try:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()
                controller.signal(stem.Signal.NEWNYM)
                time.sleep(2)  # Esperar a que Tor cambie la IP
                print("[Tor] Identidad renovada - Nueva IP asignada")
                return True
        except:
            print("[Tor] No se pudo renovar identidad")
            return False
    
    def get_current_ip(self):
        """Obtiene IP actual vía Tor"""
        try:
            response = self.session.get('http://httpbin.org/ip', timeout=10)
            return response.json()['origin']
        except:
            return "Desconocida"
    
    def anonimize_request(self, url, method='GET', data=None):
        """Realiza petición anónima"""
        try:
            if method == 'GET':
                response = self.session.get(url, timeout=15)
            else:
                response = self.session.post(url, data=data, timeout=15)
            
            return response
        except:
            return None
