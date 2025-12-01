@@ -40,7 +40,6 @@ def wrapped_init(
 
         def context_aware_initializer() -> None:
             """"""Initializer that sets up the captured context in each worker thread.""""""
-            logger.debug(""[ConcurrentFuturesInstrumentor] Setting up context in worker thread"")
 
             # Set the main context variables in this thread
             for var, value in main_context.items():
@@ -60,8 +59,6 @@ def context_aware_initializer() -> None:
                     logger.error(f""[ConcurrentFuturesInstrumentor] Error in user initializer: {e}"")
                     raise
 
-            logger.debug(""[ConcurrentFuturesInstrumentor] Worker thread context setup complete"")
-
         # Create executor with context-aware initializer
         prefix = f""AgentOps-{thread_name_prefix}"" if thread_name_prefix else ""AgentOps-Thread""
 
@@ -74,8 +71,6 @@ def context_aware_initializer() -> None:
             initargs=(),  # We handle initargs in our wrapper
         )
 
-        logger.debug(""[ConcurrentFuturesInstrumentor] ThreadPoolExecutor initialized with context propagation"")
-
     return wrapped_init
 
 
@@ -85,8 +80,7 @@ def _context_propagating_submit(original_submit: Callable) -> Callable:
     @functools.wraps(original_submit)
     def wrapped_submit(self: ThreadPoolExecutor, func: Callable[..., R], *args: Any, **kwargs: Any) -> Future[R]:
         # Log the submission
-        func_name = getattr(func, ""__name__"", str(func))
-        logger.debug(f""[ConcurrentFuturesInstrumentor] Submitting function: {func_name}"")
+        func_name = getattr(func, ""__name__"", str(func))  # noqa: F841
 
         # The context propagation is handled by the initializer, so we can submit normally
         # But we can add additional logging or monitoring here if needed