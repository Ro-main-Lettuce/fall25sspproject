@@ -20,7 +20,7 @@
 
 def test_vlmrun_invoice():
     invoice_url = (
-        ""https://storage.googleapis.com/vlm-data-public-prod/hub/examples/document.invoice-extraction/invoice_1.jpg""
+        ""https://storage.googleapis.com/vlm-data-public-prod/hub/examples/document.invoice/invoice_1.jpg""
     )
     invoice_image = remote_image(invoice_url)
     domain = ""document.invoice""