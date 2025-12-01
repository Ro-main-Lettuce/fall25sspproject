@@ -125,17 +125,6 @@ def generate_spec(
         ]
     )
 
-    # Server object type definitions
-    class ServerVariables(t.TypedDict, total=False):
-        enum: t.List[str]
-        default: str
-        description: str
-
-    class ServerObject(t.TypedDict):
-        url: str
-        description: t.NotRequired[str]
-        variables: t.NotRequired[t.Dict[str, ServerVariables]]
-
     def join_path(prefix: str, path: str) -> str:
         return f""{prefix.rstrip('/')}/{path.lstrip('/')}""
 
@@ -185,81 +174,56 @@ def convert_schema(
         Returns:
             Schema or Reference object
         """"""
-        if depth > 100:  # Prevent infinite recursion
-            return Schema(type=""object"")
-        if isinstance(schema_data, (Schema, Reference)):
-            return schema_data
-        if not isinstance(schema_data, dict):
-            return Schema(type=""object"")
+        MAX_DEPTH = 5  # Reduced depth limit to prevent recursion errors
 
-        # Add recursion depth limit
-        MAX_DEPTH = 100
         if depth > MAX_DEPTH:
             return Schema(type=""object"")
-
-        # Handle non-dict inputs
+        if isinstance(schema_data, (Schema, Reference)):
+            return schema_data
         if not isinstance(schema_data, dict):
             return Schema(type=""object"")
 
-        # Create a copy to avoid modifying input
-        schema_dict: dict[str, t.Any] = dict(schema_data)
+        schema_dict = dict(schema_data)
         if ""$ref"" in schema_dict:
             return Reference(ref=str(schema_dict[""$ref""]))
 
         # Handle nested schemas in properties
         if ""properties"" in schema_dict:
-            properties: dict[str, t.Any] = schema_dict.get(""properties"", {})
-            if isinstance(properties, dict):
+            props_dict = t.cast(
+                dict[str, dict[str, t.Any]], schema_dict.get(""properties"", {})
+            )
+            if isinstance(props_dict, dict):
                 converted_props: dict[str, t.Union[Schema, Reference]] = {}
-                for prop_name, prop_schema in properties.items():
-                    prop_key = str(prop_name)
-                    if isinstance(prop_schema, (dict, Schema, Reference)):
-                        # Break potential infinite recursion with depth limit
-                        if depth < MAX_DEPTH:
-                            converted_props[prop_key] = convert_schema(
-                                t.cast(
-                                    t.Union[Schema, Reference, dict[str, t.Any]],
-                                    prop_schema,
-                                ),
-                                depth + 1,
-                            )
-                        else:
-                            converted_props[prop_key] = Schema(type=""object"")
+
+                for name, prop_data in props_dict.items():
+                    prop_key = str(name)
+                    if isinstance(prop_data, (dict, Schema, Reference)):
+                        converted_props[prop_key] = convert_schema(prop_data, depth + 1)
                     else:
                         converted_props[prop_key] = Schema(type=""object"")
+
                 schema_dict[""properties""] = converted_props
 
         # Handle array items
         if ""items"" in schema_dict:
-            items: t.Any = schema_dict.get(""items"")
-            if isinstance(items, (dict, Schema, Reference)):
-                # Break potential infinite recursion with depth limit
-                if depth < MAX_DEPTH:
-                    schema_dict[""items""] = convert_schema(
-                        t.cast(t.Union[Schema, Reference, dict[str, t.Any]], items),
-                        depth + 1,
-                    )
-                else:
-                    schema_dict[""items""] = Schema(type=""object"")
-            elif isinstance(items, list):
+            items_data = schema_dict.get(""items"")
+            if isinstance(items_data, (dict, Schema, Reference)):
+                items_schema = t.cast(
+                    t.Union[Schema, Reference, dict[str, t.Any]], items_data
+                )
+                schema_dict[""items""] = convert_schema(items_schema, depth + 1)
+            elif isinstance(items_data, list):
+                items_list = t.cast(
+                    list[t.Union[dict[str, t.Any], Schema, Reference]], items_data
+                )
                 converted_items: list[t.Union[Schema, Reference]] = []
-                for item in t.cast(list[t.Any], items):
-                    if isinstance(item, (dict, Schema, Reference)):
-                        # Break potential infinite recursion with depth limit
-                        if depth < MAX_DEPTH:
-                            converted_items.append(
-                                convert_schema(
-                                    t.cast(
-                                        t.Union[Schema, Reference, dict[str, t.Any]],
-                                        item,
-                                    ),
-                                    depth + 1,
-                                )
-                            )
-                        else:
-                            converted_items.append(Schema(type=""object""))
+
+                for item_data in items_list:
+                    if isinstance(item_data, (dict, Schema, Reference)):
+                        converted_items.append(convert_schema(item_data, depth + 1))
                     else:
                         converted_items.append(Schema(type=""object""))
+
                 schema_dict[""items""] = converted_items
 
         try:
@@ -333,14 +297,8 @@ def convert_schema(
                 f""Error applying OpenAPI info overrides: {e}. Using defaults.""
             )
 
-    # Prepare servers configuration with proper OpenAPI types
-    initial_server = {""url"": ""."", ""description"": ""Default server""}
-    servers = [initial_server]
-
-    # Initialize components first
+    # Initialize components with proper validation
     components = Components(schemas={})
-
-    # Validate components if present in overrides
     if svc.openapi_service_overrides and ""components"" in svc.openapi_service_overrides:
         override_components = t.cast(
             t.Dict[str, t.Any], svc.openapi_service_overrides.get(""components"", {})
@@ -448,27 +406,18 @@ def convert_schema(
     # Handle server overrides with proper type checking and error handling
     if svc.openapi_service_overrides and ""servers"" in svc.openapi_service_overrides:
         try:
-            servers_raw = t.cast(
-                t.Any, svc.openapi_service_overrides.get(""servers"", [])
-            )
-            if not isinstance(servers_raw, list):
-                logger.warning(
-                    f""Invalid servers override type: expected list, got {type(servers_raw).__name__}""
-                )
-                return spec
-
-            # Initialize validated servers list
-            validated_servers: t.List[t.Dict[str, t.Any]] = []
-
-            # Validate servers list
+            servers_raw = svc.openapi_service_overrides.get(""servers"", [])
             if not isinstance(servers_raw, list):
                 logger.warning(
                     f""Invalid servers override type: expected list, got {type(servers_raw).__name__}""
                 )
                 return spec
 
             # Process each server entry
-            for server_entry in t.cast(t.List[t.Any], servers_raw):
+            validated_servers: list[dict[str, t.Any]] = []
+            server_entries = t.cast(list[dict[str, t.Any]], servers_raw)
+
+            for server_entry in server_entries:
                 if not isinstance(server_entry, dict):
                     logger.warning(
                         f""Invalid server object type: expected dict, got {type(server_entry).__name__}""
@@ -480,48 +429,52 @@ def convert_schema(
                     continue
 
                 try:
-                    server_dict = t.cast(t.Dict[str, t.Any], server_entry)
-
-                    # Create server object with validated fields
-                    server_data: t.Dict[str, t.Any] = {""url"": str(server_dict[""url""])}
+                    server_data: dict[str, t.Any] = {""url"": str(server_entry[""url""])}
 
                     # Validate optional fields
-                    if ""description"" in server_dict:
-                        desc = server_dict[""description""]
+                    if ""description"" in server_entry:
+                        desc = server_entry[""description""]
                         if isinstance(desc, (str, int, float, bool)):
                             server_data[""description""] = str(desc)
 
                     # Validate variables if present
-                    if ""variables"" in server_dict:
-                        vars_data = server_dict[""variables""]
-                        if isinstance(vars_data, dict):
-                            validated_vars: t.Dict[str, t.Dict[str, t.Any]] = {}
-
-                            for var_name, var_def in t.cast(
-                                t.Dict[str, t.Any], vars_data
-                            ).items():
+                    if ""variables"" in server_entry:
+                        vars_dict = t.cast(
+                            dict[str, dict[str, t.Any]],
+                            server_entry.get(""variables"", {}),
+                        )
+                        if isinstance(vars_dict, dict):
+                            validated_vars: dict[str, dict[str, str]] = {}
+
+                            for var_name, var_def in vars_dict.items():
                                 if isinstance(var_def, dict):
-                                    var_dict = t.cast(t.Dict[str, t.Any], var_def)
-                                    var_obj: t.Dict[str, t.Any] = {}
+                                    var_obj: dict[str, str] = {}
 
-                                    # Validate required fields
-                                    if ""default"" in var_dict:
-                                        var_obj[""default""] = str(var_dict[""default""])
+                                    if ""default"" in var_def:
+                                        default_val = var_def.get(""default"")
+                                        if default_val is not None:
+                                            var_obj[""default""] = str(default_val)
 
-                                    # Validate optional fields
-                                    if ""enum"" in var_dict and isinstance(
-                                        var_dict[""enum""], list
-                                    ):
-                                        enum_values = t.cast(
-                                            t.List[t.Any], var_dict[""enum""]
-                                        )
-                                        var_obj[""enum""] = [str(v) for v in enum_values]
-                                    if ""description"" in var_dict:
-                                        var_obj[""description""] = str(
-                                            var_dict[""description""]
+                                    if ""enum"" in var_def:
+                                        enum_vals = t.cast(
+                                            list[t.Any], var_def.get(""enum"", [])
                                         )
-
-                                    validated_vars[str(var_name)] = var_obj
+                                        if isinstance(enum_vals, list):
+                                            var_obj[""enum""] = (
+                                                ""[""
+                                                + "", "".join(
+                                                    str(val) for val in enum_vals
+                                                )
+                                                + ""]""
+                                            )
+
+                                    if ""description"" in var_def:
+                                        desc_val = var_def.get(""description"")
+                                        if desc_val is not None:
+                                            var_obj[""description""] = str(desc_val)
+
+                                    if var_obj:
+                                        validated_vars[str(var_name)] = var_obj
 
                             if validated_vars:
                                 server_data[""variables""] = validated_vars
@@ -531,75 +484,36 @@ def convert_schema(
                     logger.warning(f""Error validating server object: {err}"")
 
             if validated_servers:
-                spec.servers = validated_servers  # type: ignore
+                spec.servers = validated_servers
         except Exception as e:
             logger.warning(f""Error processing server overrides: {e}"")
 
-    return spec
-
-    # Create base specification with properly typed components
-    # Convert servers to the format expected by OpenAPISpecification
-    final_servers: t.List[t.Dict[str, t.Any]] = [
-        {k: v for k, v in server.items()} for server in servers
-    ]
-
-    spec = OpenAPISpecification(
-        openapi=openapi_version,
-        tags=[APP_TAG, INFRA_TAG],
-        components=components,
-        info=info,
-        servers=final_servers,
-        paths={
-            # setup infra endpoints
-            **make_infra_endpoints(),
-            # setup inference endpoints
-            **_get_api_routes(svc),
-            **mounted_app_paths,
-        },
-    )
-
-    # Apply remaining service-level overrides
-    if svc.openapi_service_overrides:
-        if ""servers"" in overrides:
-            override_servers = overrides[""servers""]
-            if isinstance(override_servers, list):
-                # Validate server objects
-                validated_servers: t.List[ServerObject] = []
-                for server_entry in override_servers:
-                    if isinstance(server_entry, dict) and ""url"" in server_entry:
-                        server_obj: t.Dict[str, t.Any] = {
-                            ""url"": str(server_entry[""url""])
-                        }
-                        if ""description"" in server_entry:
-                            server_obj[""description""] = str(server_entry[""description""])
-                        if ""variables"" in server_entry and isinstance(
-                            server_entry[""variables""], dict
-                        ):
-                            server_obj[""variables""] = server_entry[""variables""]
-                        validated_servers.append(t.cast(ServerObject, server_obj))
-                if validated_servers:
-                    spec.servers = validated_servers
-
-        if ""tags"" in overrides:
-            tags = overrides[""tags""]
-            if isinstance(tags, list):
-                # Ensure we keep the required APP_TAG and INFRA_TAG
-                validated_tags = []
-                for tag in tags:
-                    if isinstance(tag, dict) and ""name"" in tag:
-                        try:
-                            validated_tags.append(Tag(**tag))
-                        except (TypeError, ValueError):
-                            continue
-                    elif isinstance(tag, Tag):
-                        validated_tags.append(tag)
-                if validated_tags:
-                    spec.tags = [APP_TAG, INFRA_TAG] + validated_tags
+    # Handle tags with proper validation
+    if svc.openapi_service_overrides and ""tags"" in svc.openapi_service_overrides:
+        tag_list = t.cast(
+            list[t.Union[dict[str, t.Any], Tag]], svc.openapi_service_overrides[""tags""]
+        )
+        if isinstance(tag_list, list):
+            # Ensure we keep the required APP_TAG and INFRA_TAG
+            validated_tags: list[Tag] = []
+            for tag_item in tag_list:
+                if isinstance(tag_item, dict) and ""name"" in tag_item:
+                    try:
+                        validated_tags.append(Tag(**tag_item))
+                    except (TypeError, ValueError) as e:
+                        logger.warning(f""Invalid tag definition: {e}"")
+                        continue
+                elif isinstance(tag_item, Tag):
+                    validated_tags.append(tag_item)
+            if validated_tags:
+                spec.tags = [APP_TAG, INFRA_TAG] + validated_tags
 
     return spec
 
 
-class TaskStatusResponse(BaseModel):
+class TaskStatusResponse(BaseModel):  # type: ignore[misc]
+    """"""Response model for task status endpoint.""""""
+
     task_id: str
     status: t.Literal[""in_progress"", ""success"", ""failure"", ""cancelled""]
     created_at: str