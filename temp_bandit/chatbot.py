@@ -246,5 +246,18 @@ def _(cars, get_sample_prompts, mo, my_complex_model):
     return (prompts,)
 
 
+@app.cell
+def _(mo):
+    no_bot = mo.ui.chat(model=lambda x: ""no"")
+    no_bot
+    return (no_bot,)
+
+
+@app.cell
+def _(no_bot):
+    no_bot.value
+    return
+
+
 if __name__ == ""__main__"":
     app.run()