@@ -1,7 +1,6 @@
 import pytest
-import time
-from unittest.mock import Mock, patch, MagicMock
-from crewai.llm import LLM, BatchJobStartedEvent, BatchJobCompletedEvent, BatchJobFailedEvent
+from unittest.mock import Mock, patch
+from crewai.llm import LLM
 
 
 class TestBatchMode: