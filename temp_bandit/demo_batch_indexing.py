@@ -178,7 +178,7 @@ def create_single_index(self, index_config: Dict[str, Any]) -> Optional[str]:
             
             # Process documents through pipeline
             start_time = time.time()
-            self.pipeline.process_documents(valid_documents)
+            self.pipeline.run(valid_documents)
             processing_time = time.time() - start_time
             
             print(f""✅ Index '{index_name}' created successfully!"")
@@ -383,4 +383,4 @@ def main():
 
 
 if __name__ == ""__main__"":
-    main() 
\ No newline at end of file
+    main()  
\ No newline at end of file