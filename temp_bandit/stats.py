@@ -26,14 +26,19 @@ def stats_grid() -> rx.Component:
             icon=""star"",
             class_name=""lg:!border-l !border-slate-3"",
         ),
-        stat_card(stat=f""{CONTRIBUTORS:,}+"", text=""Contributors"", icon=""fork""),
+        stat_card(
+            stat=f""{CONTRIBUTORS:,}+"",
+            text=""Contributors"",
+            icon=""fork"",
+            class_name=""lg:!border-l !border-slate-3"",
+        ),
         stat_card(
             stat=f""{DISCORD_USERS:,}+"",
             text=""Discord"",
             icon=""discord_navbar"",
             class_name=""lg:!border-r !border-slate-3"",
         ),
-        class_name=""grid grid-cols-1 lg:grid-cols-3 gap-0 grid-rows-1 w-full divide-slate-3 lg:divide-x !border-t-0 divide-y lg:divide-y-0"",
+        class_name=""grid grid-cols-1 lg:grid-cols-3 gap-0 grid-rows-1 w-full divide-slate-3 lg:divide-x !border-t-0 divide-y lg:divide-y-0 lg:border-b border-slate-3"",
     )
 
 