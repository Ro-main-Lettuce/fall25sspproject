@@ -221,7 +221,7 @@ def create_index_interactive(self) -> None:
             
             # Process documents through pipeline
             print(""📚 Processing documents..."")
-            self.pipeline.process_documents(documents)
+            self.pipeline.run(documents)
             
             print(f""
✅ Index '{index_name}' created successfully!"")
             print(f""Index ID: {index_id}"")
@@ -300,7 +300,7 @@ def batch_create_from_config(self, config_file: str) -> None:
                 self.db.add_document_to_index(index_id, filename, doc_path)
             
             # Process documents
-            self.pipeline.process_documents(valid_documents)
+            self.pipeline.run(valid_documents)
             
             print(f""✅ Batch index '{index_name}' created successfully!"")
             print(f""Index ID: {index_id}"")
@@ -369,4 +369,4 @@ def main():
 
 
 if __name__ == ""__main__"":
-    main() 
\ No newline at end of file
+    main()  
\ No newline at end of file