@@ -221,15 +221,15 @@ async def _execute_query(
                 logger.warning(f""Query failed, attempt {attempt + 1}: {str(e)}"")
                 continue
 
-    async def _run(
+    async def _arun(
         self,
         query: str,
         database: Optional[str] = None,
         snowflake_schema: Optional[str] = None,
         timeout: int = 300,
         **kwargs: Any,
     ) -> Any:
-        """"""Execute the search query.""""""
+        """"""Execute the search query asynchronously.""""""
 
         try:
             # Override database/schema if provided
@@ -243,6 +243,65 @@ async def _run(
         except Exception as e:
             logger.error(f""Error executing query: {str(e)}"")
             raise
+            
+    def _run(
+        self,
+        query: str,
+        database: Optional[str] = None,
+        snowflake_schema: Optional[str] = None,
+        timeout: int = 300,
+        **kwargs: Any,
+    ) -> Any:
+        """"""Execute the search query.
+        
+        This method detects whether it's being called from an async context:
+        - In async context: returns the coroutine directly
+        - In sync context: runs the coroutine and returns the result
+        """"""
+        import asyncio
+        import sys
+        import inspect
+
+        try:
+            try:
+                asyncio.get_running_loop()
+                return self._arun(
+                    query=query,
+                    database=database,
+                    snowflake_schema=snowflake_schema,
+                    timeout=timeout,
+                    **kwargs
+                )
+            except RuntimeError:
+                
+                conn = self._create_connection()
+                try:
+                    cursor = conn.cursor()
+                    
+                    # Override database/schema if provided
+                    if database:
+                        cursor.execute(f""USE DATABASE {database}"")
+                    if snowflake_schema:
+                        cursor.execute(f""USE SCHEMA {snowflake_schema}"")
+                    
+                    cursor.execute(query, timeout=timeout)
+                    
+                    if not cursor.description:
+                        return []
+                    
+                    columns = [col[0] for col in cursor.description]
+                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
+                    
+                    if self.enable_caching:
+                        _query_cache[self._get_cache_key(query, timeout)] = results
+                    
+                    return results
+                finally:
+                    cursor.close()
+                    conn.close()
+        except Exception as e:
+            logger.error(f""Error executing query synchronously: {str(e)}"")
+            raise
 
     def __del__(self):
         """"""Cleanup connections on deletion.""""""