import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

class WAFDetectorML:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.X_train = self.prepare_training_data()
        self.train_model()
    
    def extract_features(self, response):
        """Extrae características de la respuesta"""
        features = []
        headers = response.headers
        text = response.text.lower()
        
        # Features de headers (basado en wafw00f)
        features.append(1 if 'cloudflare' in str(headers) else 0)
        features.append(1 if 'x-sucuri-id' in headers else 0)
        features.append(1 if 'x-akamai-transformed' in headers else 0)
        features.append(1 if 'server: awselb' in str(headers) else 0)
        features.append(1 if 'x-mod-pagespeed' in headers else 0)
        
        # Features de texto
        waf_signatures = [
            'modsecurity', 'owasp', 'cloudflare', 'sucuri', 
            'incapsula', 'f5', 'imperva', 'fortinet', 
            'barracuda', 'radware', 'akamai'
        ]
        
        for sig in waf_signatures:
            features.append(1 if sig in text else 0)
        
        # Features de status code
        features.append(response.status_code)
        
        # Tiempo de respuesta
        features.append(response.elapsed.total_seconds())
        
        return np.array(features).reshape(1, -1)
    
    def prepare_training_data(self):
        """Datos de entrenamiento (simulados por ahora)"""
        # Aquí normalmente cargarías datos reales
        # Por ahora, datos sintéticos
        X = []
        y = []
        
        for i in range(100):
            features = np.random.rand(50)  # 50 features
            label = np.random.randint(0, 5)  # 5 tipos de WAF
            X.append(features)
            y.append(label)
        
        return np.array(X), np.array(y)
    
    def train_model(self):
        """Entrena el modelo Random Forest"""
        X, y = self.X_train
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_scaled, y)
        print("[ML] Modelo de detección de WAF entrenado")
    
    def predict_waf(self, response):
        """Predice qué WAF está presente"""
        if not self.model:
            return "Desconocido"
        
        features = self.extract_features(response)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)
        
        waf_types = {
            0: "Cloudflare",
            1: "ModSecurity/OWASP",
            2: "AWS WAF",
            3: "Sucuri/Incapsula",
            4: "F5/Imperva",
            5: "Ninguno detectado"
        }
        
        return waf_types.get(prediction[0], "WAF Desconocido")
    
    def generate_bypass_strategy(self, waf_type):
        """Genera estrategias específicas por WAF"""
        strategies = {
            "Cloudflare": [
                "Usar cloudscraper",
                "Rotar user-agents cada request",
                "Añadir delays de 2-5 segundos",
                "Usar Tor para rotar IPs"
            ],
            "ModSecurity/OWASP": [
                "Usar payloads en múltiples casos",
                "Evitar caracteres especiales",
                "Usar comentarios SQL /*!50000*/",
                "Fragmentar payloads entre parámetros"
            ],
            "AWS WAF": [
                "Rate limiting: 1 request/segundo",
                "Variar patrones de ataque",
                "Usar encoding doble URL",
                "Session persistence"
            ]
        }
        
        return strategies.get(waf_type, ["Estrategia genérica de bypass"])
