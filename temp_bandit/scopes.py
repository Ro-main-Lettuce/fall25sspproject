@@ -72,12 +72,13 @@
     ""MetafieldArticles"": (""read_online_store_pages"",),
     ""Blogs"": (""read_online_store_pages"",),
     ""MetafieldBlogs"": (""read_online_store_pages"",),
+    # SCOPE: read_shipping
+    ""Countries"": (""read_shipping"",),
 }
 
 ALWAYS_PERMITTED_STREAMS: List[str] = [
     ""MetafieldShops"",
     ""Shop"",
-    ""Countries"",
 ]
 
 