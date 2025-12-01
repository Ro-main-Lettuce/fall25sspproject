@@ -63,7 +63,6 @@ def __init__(self, client, project, name=None, entity=None, per_page=50):
 
     @property
     def length(self):
-        # TODO: Add the count the backend
         if self.last_response:
             return len(self.objects)
         else:
@@ -129,11 +128,20 @@ def __init__(self, client, attrs, entity=None, project=None):
         self.entity = entity
         self.query_generator = public.QueryGenerator()
         super().__init__(dict(attrs))
-        self._attrs[""spec""] = json.loads(self._attrs[""spec""])
+        if ""spec"" in self._attrs:
+            if isinstance(self._attrs[""spec""], str):
+                self._attrs[""spec""] = json.loads(self._attrs[""spec""])
+        else:
+            self._attrs[""spec""] = {}
+
+    @property
+    def spec(self):
+        spec_dict = self._attrs.get(""spec"", {})
+        return None if not spec_dict else spec_dict
 
     @property
     def sections(self):
-        return self.spec[""panelGroups""]
+        return self.spec.get(""panelGroups"", []) if self.spec else []
 
     def runs(self, section, per_page=50, only_selected=True):
         run_set_idx = section.get(""openRunSet"", 0)
@@ -145,7 +153,6 @@ def runs(self, section, per_page=50, only_selected=True):
             order = ""-"" + order
         filters = self.query_generator.filter_to_mongo(run_set[""filters""])
         if only_selected:
-            # TODO: handle this not always existing
             filters[""$or""][0][""$and""].append(
                 {""name"": {""$in"": run_set[""selections""][""tree""]}}
             )
@@ -188,6 +195,8 @@ def created_at(self):
 
     @property
     def url(self):
+        if not self.client or not self.entity or not self.project or not self.display_name or not self.id:
+            return None
         return self.client.app_url + ""/"".join(
             [
                 self.entity,
@@ -237,7 +246,6 @@ class PythonMongoishQueryGenerator:
         ""Relative Time (Wall)"": ""_absolute_runtime"",
         ""Relative Time (Process)"": ""_runtime"",
         ""Wall Time"": ""_timestamp"",
-        # ""GroupedRuns"": ""__wb_group_by_all""
     }
     FRONTEND_NAME_MAPPING_REVERSED = {v: k for k, v in FRONTEND_NAME_MAPPING.items()}
     AST_OPERATORS = {
@@ -268,12 +276,10 @@ def __init__(self, run_set):
         self.panel_metrics_helper = PanelMetricsHelper()
 
     def _handle_compare(self, node):
-        # only left side can be a col
         left = self.front_to_back(self._handle_fields(node.left))
         op = self._handle_ops(node.ops[0])
         right = self._handle_fields(node.comparators[0])
 
-        # Eq has no op for some reason
         if op == ""="":
             return {left: right}
         else:
@@ -303,7 +309,6 @@ def _replace_numeric_dots(self, s):
                     and right.isdigit()  # .2
                 ):
                     numeric_dots.append(i)
-        # Edge: Catch number ending in dot at end of string
         if s[-2].isdigit() and s[-1] == ""."":
             numeric_dots.append(len(s) - 1)
         numeric_dots = [-1] + numeric_dots + [len(s)]
@@ -365,14 +370,12 @@ def back_to_front(self, name):
         elif (
             name.startswith(""config."") and "".value"" in name
         ):  # may be brittle: originally ""endswith"", but that doesn't work with nested keys...
-            # strip is weird sometimes (??)
             return name.replace(""config."", """").replace("".value"", """")
         elif name.startswith(""summary_metrics.""):
             return name.replace(""summary_metrics."", """")
         wandb.termerror(f""Unknown token: {name}"")
         return name
 
-    # These are only used for ParallelCoordinatesPlot because it has weird backend names...
     def pc_front_to_back(self, name):
         name, *rest = name.split(""."")
         rest = ""."" + ""."".join(rest) if rest else """"
@@ -430,20 +433,17 @@ def back_to_front(self, name):
             return self.FRONTEND_NAME_MAPPING_REVERSED[name]
         return name
 
-    # ScatterPlot and ParallelCoords have weird conventions
     def special_front_to_back(self, name):
         if name is None:
             return name
 
         name, *rest = name.split(""."")
         rest = ""."" + ""."".join(rest) if rest else """"
 
-        # special case for config
         if name.startswith(""c::""):
             name = name[3:]
             return f""config:{name}.value{rest}""
 
-        # special case for summary
         if name.startswith(""s::""):
             name = name[3:] + rest
             return f""summary:{name}""