@@ -1450,6 +1450,7 @@ def start_safekeeper(self, i):
             str(i),
             ""--broker-endpoint"",
             self.fake_broker_endpoint,
+            ""--dev"",
         ]
         log.info(f'Running command ""{"" "".join(cmd)}""')
 