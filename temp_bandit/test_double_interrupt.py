@@ -1,6 +1,7 @@
 import multiprocessing as mp
 import sys
 import time
+from typing import Callable
 from unittest.mock import patch
 
 import pytest
@@ -12,8 +13,12 @@
 from marimo._server.file_manager import AppFileManager
 from marimo._server.ids import ConsumerId
 from marimo._server.model import ConnectionState
-from marimo._server.sessions import QueueManager, Session, SessionMode, SessionConsumer
-from typing import Callable
+from marimo._server.sessions import (
+    QueueManager,
+    Session,
+    SessionConsumer,
+    SessionMode,
+)
 
 
 class MockSessionConsumer(SessionConsumer):