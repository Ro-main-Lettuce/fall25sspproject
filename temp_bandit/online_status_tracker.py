@@ -19,7 +19,7 @@ class OnlineStatusTracker:
     num_api_errors: int = 0
     num_other_errors: int = 0
     num_rate_limit_errors: int = 0
-    available_request_capacity: float = 0
+    available_request_capacity: float = 1.0
     available_token_capacity: float = 0
     last_update_time: float = field(default_factory=time.time)
     max_requests_per_minute: int = 0
@@ -29,6 +29,7 @@ class OnlineStatusTracker:
     time_of_last_rate_limit_error: float = field(default=0.0)
 
     def __str__(self):
+        """"""String representation of the status tracker.""""""
         return (
             f""Tasks - Started: {self.num_tasks_started}, ""
             f""In Progress: {self.num_tasks_in_progress}, ""
@@ -42,30 +43,26 @@ def __str__(self):
         )
 
     def update_capacity(self):
-        """"""Update available capacity based on time elapsed""""""
+        """"""Update available capacity based on time elapsed.""""""
         current_time = time.time()
         seconds_since_update = current_time - self.last_update_time
 
         self.available_request_capacity = min(
-            self.available_request_capacity
-            + self.max_requests_per_minute * seconds_since_update / 60.0,
+            self.available_request_capacity + self.max_requests_per_minute * seconds_since_update / 60.0,
             self.max_requests_per_minute,
         )
 
         self.available_token_capacity = min(
-            self.available_token_capacity
-            + self.max_tokens_per_minute * seconds_since_update / 60.0,
+            self.available_token_capacity + self.max_tokens_per_minute * seconds_since_update / 60.0,
             self.max_tokens_per_minute,
         )
 
         self.last_update_time = current_time
 
     def has_capacity(self, token_estimate: int) -> bool:
-        """"""Check if there's enough capacity for a request""""""
+        """"""Check if there's enough capacity for a request.""""""
         self.update_capacity()
-        has_capacity = (
-            self.available_request_capacity >= 1 and self.available_token_capacity >= token_estimate
-        )
+        has_capacity = self.available_request_capacity >= 1 and self.available_token_capacity >= token_estimate
         if not has_capacity:
             logger.debug(
                 f""No capacity for request with {token_estimate} tokens. ""
@@ -75,6 +72,6 @@ def has_capacity(self, token_estimate: int) -> bool:
         return has_capacity
 
     def consume_capacity(self, token_estimate: int):
-        """"""Consume capacity for a request""""""
+        """"""Consume capacity for a request.""""""
         self.available_request_capacity -= 1
         self.available_token_capacity -= token_estimate