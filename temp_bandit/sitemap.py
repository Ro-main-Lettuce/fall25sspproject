@@ -193,7 +193,7 @@ def sitemap_task(unevaluated_pages: Sequence[""UnevaluatedPage""]) -> tuple[str, s
     )
 
 
-class Plugin(PluginBase):
+class SitemapPlugin(PluginBase):
     """"""Sitemap plugin for Reflex.""""""
 
     def pre_compile(self, **context):
@@ -204,3 +204,6 @@ def pre_compile(self, **context):
         """"""
         unevaluated_pages = context.get(""unevaluated_pages"", [])
         context[""add_save_task""](sitemap_task, unevaluated_pages)
+
+
+Plugin = SitemapPlugin