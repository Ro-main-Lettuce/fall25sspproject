@@ -85,7 +85,14 @@ def favicons_links() -> list[rx.Component]:
     ]
 
 
-def create_meta_tags(title: str, description: str, image: str) -> list[rx.Component]:
+def create_meta_tags(title: str, description: str, image: str, url: str = None) -> list[rx.Component]:
+    page_url = url if url else REFLEX_DOMAIN_URL
+    
+    if image and not image.startswith(('http://', 'https://')):
+        image_url = f""https://reflex.dev{'' if image.startswith('/') else '/'}{image}""
+    else:
+        image_url = image
+    
     return [
         # HTML Meta Tags
         {""name"": ""application-name"", ""content"": ""Reflex""},
@@ -98,23 +105,23 @@ def create_meta_tags(title: str, description: str, image: str) -> list[rx.Compon
             ""content"": description,
         },
         # Facebook Meta Tags
-        {""property"": ""og:url"", ""content"": REFLEX_DOMAIN_URL},
+        {""property"": ""og:url"", ""content"": page_url},
         {""property"": ""og:type"", ""content"": ""website""},
         {""property"": ""og:title"", ""content"": title},
         {
             ""property"": ""og:description"",
             ""content"": description,
         },
-        {""property"": ""og:image"", ""content"": image},
+        {""property"": ""og:image"", ""content"": image_url},
         # Twitter Meta Tags
         {""name"": ""twitter:card"", ""content"": ""summary_large_image""},
         {""property"": ""twitter:domain"", ""content"": REFLEX_DOMAIN},
-        {""property"": ""twitter:url"", ""content"": REFLEX_DOMAIN_URL},
+        {""property"": ""twitter:url"", ""content"": page_url},
         {""name"": ""twitter:title"", ""content"": title},
         {
             ""name"": ""twitter:description"",
             ""content"": description,
         },
-        {""name"": ""twitter:image"", ""content"": image},
+        {""name"": ""twitter:image"", ""content"": image_url},
         {""name"": ""twitter:creator"", ""content"": TWITTER_CREATOR},
     ]