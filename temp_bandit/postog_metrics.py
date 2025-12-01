@@ -4,7 +4,7 @@
 import httpx
 from posthog import Posthog
 from reflex.utils.console import log
-from pcweb.constants import POSTHOG_API_KEY
+from pcweb.constants import POSTHOG_API_KEY, SLACK_DEMO_WEBHOOK_URL
 
 try:
     posthog = Posthog(POSTHOG_API_KEY, host=""https://us.i.posthog.com"")
@@ -35,6 +35,7 @@ class DemoEvent(PosthogEvent):
     num_employees: str
     internal_tools: str
     referral_source: str
+    phone_number: str = """"
 
 
 async def send_data_to_posthog(event_instance: PosthogEvent):
@@ -59,3 +60,34 @@ async def send_data_to_posthog(event_instance: PosthogEvent):
             response.raise_for_status()
     except Exception:
         log(""Error sending data to PostHog"")
+
+
+async def send_data_to_slack(event_instance: DemoEvent):
+    """"""Send demo form data to Slack webhook.
+    
+    Args:
+        event_instance: An instance of DemoEvent with form data.
+    """"""
+    slack_payload = {
+        ""lookingToBuild"": event_instance.internal_tools,
+        ""businessEmail"": event_instance.company_email,
+        ""howDidYouHear"": event_instance.referral_source,
+        ""linkedinUrl"": event_instance.linkedin_url,
+        ""jobTitle"": event_instance.job_title,
+        ""numEmployees"": event_instance.num_employees,
+        ""companyName"": event_instance.company_name,
+        ""firstName"": event_instance.first_name,
+        ""lastName"": event_instance.last_name,
+        ""phoneNumber"": event_instance.phone_number
+    }
+    
+    try:
+        async with httpx.AsyncClient() as client:
+            response = await client.post(
+                SLACK_DEMO_WEBHOOK_URL,
+                json=slack_payload,
+                headers={""Content-Type"": ""application/json""}
+            )
+            response.raise_for_status()
+    except Exception as e:
+        log(f""Error sending data to Slack webhook: {e}"")