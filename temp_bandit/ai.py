@@ -45,4 +45,19 @@ def get_sidebar_items_ai_builder_overview():
     ]
 
 
+def get_sidebar_items_mcp():
+    from pcweb.pages.docs import ai_builder
+
+    return [
+        create_item(
+            ""MCP Integration"",
+            children=[
+                ai_builder.integrations.mcp_overview,
+                ai_builder.integrations.mcp_installation,
+            ],
+        ),
+    ]
+
+
 ai_builder_overview_items = get_sidebar_items_ai_builder_overview()
+mcp_items = get_sidebar_items_mcp()