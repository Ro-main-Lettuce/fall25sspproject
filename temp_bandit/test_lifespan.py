@@ -6,7 +6,6 @@
 import httpx
 import pytest
 from selenium.webdriver.common.by import By
-from starlette.responses import JSONResponse
 
 from reflex.testing import AppHarness
 
@@ -25,6 +24,8 @@ def LifespanApp(
     import asyncio
     from contextlib import asynccontextmanager
 
+    from starlette.responses import JSONResponse
+
     import reflex as rx
 
     lifespan_task_global = 0