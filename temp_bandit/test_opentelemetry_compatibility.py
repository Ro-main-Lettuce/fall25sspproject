@@ -90,6 +90,7 @@ def test_span_creation():
     import os
 
     from opentelemetry import trace
+
     from src.crewai.telemetry.telemetry import Telemetry
     
     # Ensure telemetry is enabled for this test