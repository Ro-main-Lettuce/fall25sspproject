@@ -1,7 +1,10 @@
-import pytest
 from unittest.mock import patch
+
+import pytest
+
 from crewai.utilities.embedding_configurator import EmbeddingConfigurator
 
+
 @pytest.mark.parametrize(
     ""test_case"",
     [