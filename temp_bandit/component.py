@@ -1081,7 +1081,7 @@ def multi_docs(path, comp, component_list, title):
         component_docs(component_tuple, comp) for component_tuple in component_list[1:]
     ]
     fname = path.strip(""/"") + "".md""
-    ll_doc_exists = os.path.exists(fname.replace("".md"", ""-ll.md""))
+    ll_doc_exists = os.path.exists(fname.replace("".md"", ""_ll.md""))
 
     active_class_name = ""font-small bg-slate-2 p-2 text-slate-11 rounded-xl shadow-large w-28 cursor-default border border-slate-4 text-center""
 
@@ -1145,7 +1145,7 @@ def out():
     @docpage(set_path=path + ""low"", t=title + "" (Low Level)"")
     def ll():
         nonlocal fname
-        fname = fname.replace("".md"", ""-ll.md"")
+        fname = fname.replace("".md"", ""_ll.md"")
         d2 = Document.from_file(fname)
         toc = get_toc(d2, fname, component_list)
         return toc, rx.box(