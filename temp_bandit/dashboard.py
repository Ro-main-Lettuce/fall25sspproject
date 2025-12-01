@@ -39,6 +39,16 @@ def log_trace_url(span: Union[Span, ReadableSpan], title: Optional[str] = None)
 
     Args:
         span: The span to log the URL for.
+        title: Optional title for the trace.
     """"""
+    from agentops import get_client
+
+    try:
+        client = get_client()
+        if not client.config.log_session_replay_url:
+            return
+    except Exception:
+        return
+
     session_url = get_trace_url(span)
     logger.info(colored(f""\x1b[34mSession Replay for {title} trace: {session_url}\x1b[0m"", ""blue""))