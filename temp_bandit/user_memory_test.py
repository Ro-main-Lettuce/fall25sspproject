@@ -1,6 +1,6 @@
-import pytest
+from unittest.mock import PropertyMock, patch
 
-from unittest.mock import patch, PropertyMock
+import pytest
 
 from crewai.memory.storage.rag_storage import RAGStorage
 from crewai.memory.user.user_memory import UserMemory