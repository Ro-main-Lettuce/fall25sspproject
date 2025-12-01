@@ -36,6 +36,9 @@
 from dataclasses import dataclass
 import psutil
 
+if 'PYTHONUTF8' not in os.environ:
+    os.environ['PYTHONUTF8'] = '1'
+
 @dataclass
 class ServiceConfig:
     name: str
@@ -261,6 +264,7 @@ def start_service(self, service_name: str, config: ServiceConfig) -> bool:
         try:
             # Setup environment
             env = os.environ.copy()
+            env['PYTHONUTF8'] = '1'
             if config.env:
                 env.update(config.env)
             
@@ -504,6 +508,8 @@ def main():
     
     args = parser.parse_args()
     
+    os.environ['PYTHONUTF8'] = '1'
+    
     # Create service manager
     manager = ServiceManager(mode=args.mode)
     
@@ -538,4 +544,4 @@ def main():
         manager.shutdown()
 
 if __name__ == ""__main__"":
-    main() 
\ No newline at end of file
+    main()      
\ No newline at end of file