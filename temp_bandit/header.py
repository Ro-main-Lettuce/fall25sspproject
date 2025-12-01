@@ -11,7 +11,11 @@
 from pcweb.components.new_button import button
 from pcweb.constants import CAL_REQUEST_DEMO_URL
 from pcweb.pages.framework.views.companies import pricing_page_companies
-from pcweb.telemetry.postog_metrics import DemoEvent, send_data_to_posthog, send_data_to_slack
+from pcweb.telemetry.postog_metrics import (
+    DemoEvent,
+    send_data_to_posthog,
+    send_data_to_slack,
+)
 
 ThankYouDialogState = ClientStateVar.create(""thank_you_dialog_state"", False)
 
@@ -134,7 +138,7 @@ def submit(self, form_data: dict[str, Any]):
         linkedin_url = form_data.get(""linkedin_url"", """").strip()
         if linkedin_url:
             # Basic LinkedIn URL validation
-            linkedin_pattern = r'^https?://(www\.)?linkedin\.com/(in|company)/.+$'
+            linkedin_pattern = r""^https?://(www\.)?linkedin\.com/(in|company)/.+$""
 
             if not re.match(linkedin_pattern, linkedin_url):
                 self.banned_linkedin = True
@@ -191,11 +195,13 @@ def submit(self, form_data: dict[str, Any]):
             # Send to PostHog for all submissions
             yield QuoteFormState.send_demo_event(form_data)
 
-            yield rx.call_script(f""try {{ ko.identify('{email}'); }} catch(e) {{ console.warn('Koala identify failed:', e); }}"")
-            
+            yield rx.call_script(
+                f""try {{ ko.identify('{email}'); }} catch(e) {{ console.warn('Koala identify failed:', e); }}""
+            )
+
             if self.is_small_company():
                 yield ThankYouDialogState.push(True)
-                yield rx.redirect(""/pricing?lead=1"")
+                yield rx.redirect(""https://cal.com/team/reflex/reflexdemo"") 
                 return
 
             params = {
@@ -209,7 +215,6 @@ def submit(self, form_data: dict[str, Any]):
 
             return rx.redirect(cal_url)
 
-
     @rx.event(background=True)
     async def send_demo_event(self, form_data: dict[str, Any]):
         first_name = form_data.get(""first_name"", """")
@@ -227,10 +232,10 @@ async def send_demo_event(self, form_data: dict[str, Any]):
             referral_source=self.referral_source,
             phone_number=form_data.get(""phone_number"", """"),
         )
-        
+
         # Send to PostHog (existing)
         await send_data_to_posthog(demo_event)
-        
+
         # Send to Slack (new)
         try:
             await send_data_to_slack(demo_event)
@@ -347,8 +352,7 @@ def thank_you_modal() -> rx.Component:
                             size=""icon-sm"",
                             type=""button"",
                             class_name=""focus:outline-none"",
-                            on_click=ThankYouDialogState.set_value(False)
-
+                            on_click=ThankYouDialogState.set_value(False),
                         ),
                     ),
                     class_name=""flex flex-row items-center gap-2 justify-between w-full"",
@@ -357,19 +361,16 @@ def thank_you_modal() -> rx.Component:
                     ""We've received your submission and our team will get back to you soon. We appreciate your interest in Reflex!"",
                     class_name=""text-slate-9 font-medium text-sm"",
                 ),
-                class_name=""flex flex-col w-full gap-y-4""
+                class_name=""flex flex-col w-full gap-y-4"",
             ),
             class_name=""w-full"",
             on_interact_outside=ThankYouDialogState.set_value(False),
             on_escape_key_down=ThankYouDialogState.set_value(False),
-
         ),
-        open=ThankYouDialogState.value
+        open=ThankYouDialogState.value,
     )
 
 
-
-
 def custom_quote_form() -> rx.Component:
     """"""Custom quote form component with clean, maintainable structure.""""""
     return rx.box(
@@ -507,7 +508,15 @@ def custom_quote_form() -> rx.Component:
                         select_field(
                             ""Number of employees"",
                             ""num_employees"",
-                            [""1"", ""2-5"", ""6-10"", ""11-50"", ""51-100"", ""101-500"", ""500+""],  # Updated options
+                            [
+                                ""1"",
+                                ""2-5"",
+                                ""6-10"",
+                                ""11-50"",
+                                ""51-100"",
+                                ""101-500"",
+                                ""500+"",
+                            ],  # Updated options
                             ""500+"",
                             required=True,
                             state_var=""num_employees"",
@@ -541,7 +550,7 @@ def custom_quote_form() -> rx.Component:
                     on_submit=QuoteFormState.submit,
                     reset_on_submit=True,
                 ),
-                class_name=""relative bg-slate-1 p-6 sm:p-8 rounded-2xl border-2 border-[--violet-9] shadow-lg w-full max-w-md mx-auto lg:max-w-none lg:mx-0"",
+                class_name=""relative bg-slate-1 p-6 sm:p-8 rounded-2xl border-2 border-violet-9 shadow-lg w-full max-w-md mx-auto lg:max-w-none lg:mx-0"",
             ),
             class_name=""grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 max-w-7xl mx-auto items-start"",
         ),