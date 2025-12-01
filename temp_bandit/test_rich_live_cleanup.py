@@ -1,7 +1,4 @@
-import logging
-from io import StringIO
-from unittest.mock import MagicMock, patch
-from rich.logging import RichHandler
+from unittest.mock import patch
 from rich.tree import Tree
 from crewai.utilities.events.utils.console_formatter import ConsoleFormatter
 from crewai.utilities.events.event_listener import EventListener