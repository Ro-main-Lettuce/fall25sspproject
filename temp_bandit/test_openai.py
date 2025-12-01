@@ -25,7 +25,7 @@ def test_openai_structured_outputs_simple(openai_client):
     from vlmrun.hub.utils import encode_image, remote_image
 
     invoice_url = (
-        ""https://storage.googleapis.com/vlm-data-public-prod/hub/examples/document.invoice-extraction/invoice_1.jpg""
+        ""https://storage.googleapis.com/vlm-data-public-prod/hub/examples/document.invoice/invoice_1.jpg""
     )
     invoice_image = remote_image(invoice_url)
 