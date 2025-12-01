@@ -92,7 +92,7 @@ def parse_slp(
         with open(os.path.join(output_dir, md5), 'wb') as f:
           f.write(game_bytes)
 
-  except KeyboardInterrupt as e:
+  except KeyboardInterrupt:
     raise
   except BaseException as e:
     result.update(valid=False, reason=repr(e))
@@ -234,11 +234,11 @@ def parse_7zs(
 
   return results
 
-md5_key = 'slp_md5'
+MD5_KEY = 'slp_md5'
 
 def get_key(row: dict):
-  if md5_key in row:
-    return row[md5_key]
+  if MD5_KEY in row:
+    return row[MD5_KEY]
 
   return (row['raw'], row['name'])
 
@@ -258,7 +258,7 @@ def run_parsing(
 
   raw_db_path = os.path.join(root, 'raw.json')
   if os.path.exists(raw_db_path):
-    with open(raw_db_path) as f:
+    with open(raw_db_path, 'r') as f:
       raw_db = json.load(f)
   else:
     raw_db = []
@@ -346,20 +346,6 @@ def run_parsing(
   with open(os.path.join(root, 'parsed.pkl'), 'wb') as f:
     pickle.dump(list(by_key.values()), f)
 
-def main(_):
-  run_parsing(
-      ROOT.value,
-      num_threads=THREADS.value,
-      chunk_size_gb=CHUNK_SIZE.value,
-      in_memory=IN_MEMORY.value,
-      compression_options=dict(
-          compression=COMPRESSION.value,
-          compression_level=COMPRESSION_LEVEL.value,
-      ),
-      reprocess=REPROCESS.value,
-      dry_run=DRY_RUN.value,
-  )
-
 if __name__ == '__main__':
   ROOT = flags.DEFINE_string('root', None, 'root directory', required=True)
   # MAX_FILES = flags.DEFINE_integer('max_files', None, 'max files to process')
@@ -376,4 +362,18 @@ def main(_):
   REPROCESS = flags.DEFINE_bool('reprocess', False, 'Reprocess raw archives.')
   DRY_RUN = flags.DEFINE_bool('dry_run', False, 'dry run')
 
+  def main(_):
+    run_parsing(
+        ROOT.value,
+        num_threads=THREADS.value,
+        chunk_size_gb=CHUNK_SIZE.value,
+        in_memory=IN_MEMORY.value,
+        compression_options=dict(
+            compression=COMPRESSION.value,
+            compression_level=COMPRESSION_LEVEL.value,
+        ),
+        reprocess=REPROCESS.value,
+        dry_run=DRY_RUN.value,
+    )
+
   app.run(main)