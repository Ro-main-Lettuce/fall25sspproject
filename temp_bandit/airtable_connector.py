@@ -247,7 +247,7 @@ def _process_record(
         record: RecordDict,
         table_schema: TableSchema,
         primary_field_name: str | None,
-    ) -> Document:
+    ) -> Document | None:
         """"""Process a single Airtable record into a Document.
 
         Args:
@@ -291,6 +291,10 @@ def _process_record(
             sections.extend(field_sections)
             metadata.update(field_metadata)
 
+        if not sections:
+            logger.warning(f""No sections found for record {record_id}"")
+            return None
+
         semantic_id = (
             f""{table_name}: {primary_field_value}""
             if primary_field_value
@@ -334,7 +338,8 @@ def load_from_state(self) -> GenerateDocumentsOutput:
                 table_schema=table_schema,
                 primary_field_name=primary_field_name,
             )
-            record_documents.append(document)
+            if document:
+                record_documents.append(document)
 
             if len(record_documents) >= self.batch_size:
                 yield record_documents