@@ -72,7 +72,6 @@ def __init__(
         breakdowns: List[str] = None,
         action_breakdowns: List[str] = None,
         action_breakdowns_allow_empty: bool = False,
-        action_report_time: str = ""mixed"",
         time_increment: Optional[int] = None,
         insights_lookback_window: int = None,
         insights_job_timeout: int = 60,
@@ -92,7 +91,6 @@ def __init__(
         if breakdowns is not None:
             self.breakdowns = breakdowns
         self.time_increment = time_increment or self.time_increment
-        self.action_report_time = action_report_time
         self._new_class_name = name
         self._insights_lookback_window = insights_lookback_window
         self._insights_job_timeout = insights_job_timeout
@@ -365,7 +363,6 @@ def request_params(self, **kwargs) -> MutableMapping[str, Any]:
         req_params = {
             ""level"": self.level,
             ""action_breakdowns"": self.action_breakdowns,
-            ""action_report_time"": self.action_report_time,
             ""breakdowns"": self.breakdowns,
             ""fields"": self.fields(),
             ""time_increment"": self.time_increment,