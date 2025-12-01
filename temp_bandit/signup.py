@@ -100,4 +100,7 @@ def signup(
         self.send_contact_to_webhook(email)
         self.add_contact_to_loops(email)
         self.signed_up = True
-        return rx.toast.success(""Thanks for signing up to the Newsletter!"")
+        return [
+            rx.call_script(f""try {{ ko.identify('{email}'); }} catch(e) {{ console.warn('Koala identify failed:', e); }}""),
+            rx.toast.success(""Thanks for signing up to the Newsletter!"")
+        ]