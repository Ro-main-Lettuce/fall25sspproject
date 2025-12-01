@@ -50,7 +50,6 @@ def index():
     app.add_page(index)
     if not tailwind_version:
         config = rx.config.get_config()
-        config.tailwind = None
         config.plugins = []
     elif tailwind_version == 3:
         config = rx.config.get_config()