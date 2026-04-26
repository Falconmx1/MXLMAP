#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from core.output import banner, print_status
from core.detector import SQLDetector

class MXlmap:
    def __init__(self):
        self.version = "1.0.0"
        
    def main(self):
        banner()
        args = self.parse_arguments()
        
        print_status(f"Iniciando ataque en: {args.url}", "INFO")
        
        detector = SQLDetector(args.url)
        if detector.check_vulnerability():
            print_status("¡VULNERABLE! Ejecutando exploit...", "SUCCESS")
        else:
            print_status("No se detectó vulnerabilidad :(", "ERROR")
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='MXlmap - SQLi Tool más verga')
        parser.add_argument('-u', '--url', required=True, help='URL objetivo')
        parser.add_argument('--level', choices=['normal', 'berserker', 'stealth'], 
                           default='normal', help='Nivel de intensidad')
        parser.add_argument('--dump-all', action='store_true', help='Extraer toda la DB')
        return parser.parse_args()

if __name__ == "__main__":
    tool = MXlmap()
    tool.main()
