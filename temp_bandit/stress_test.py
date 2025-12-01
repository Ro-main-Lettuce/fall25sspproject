@@ -44,7 +44,7 @@ def setup_tables(self):
         conn = self.get_connection()
         try:
             with conn.cursor() as cur:
-                cur.execute(""CREATE EXTENSION pg_mooncake;"")
+                cur.execute(""CREATE EXTENSION IF NOT EXISTS pg_mooncake;"")
                 
                 cur.execute(""DROP TABLE IF EXISTS stress_regular CASCADE;"")
                 cur.execute(""DROP TABLE IF EXISTS stress_columnstore CASCADE;"")