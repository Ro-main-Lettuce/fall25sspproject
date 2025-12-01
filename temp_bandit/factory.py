@@ -12,10 +12,12 @@
 from functools import partial
 
 import anyio.to_thread
-import attrs
-from simple_di import Provide
-from simple_di import inject
+from attrs import define  # type: ignore
+from attrs import field  # type: ignore
+from simple_di import inject  # type: ignore
+from typing_extensions import ParamSpec
 from typing_extensions import TypeAlias
+from typing_extensions import TypeGuard
 from typing_extensions import Unpack
 
 from bentoml import Runner
@@ -38,21 +40,59 @@
 from ..models import HuggingFaceModel
 from ..models import Model
 from .config import ServiceConfig as Config
-from .dependency import Dependency
+from .types import DependencyInstance
+from .types import ServiceInstance
+from .types import T
+from .types import provide
+
+# Type variables for generic types
+_P = ParamSpec(""_P"")  # Parameters for service methods
+
+if t.TYPE_CHECKING:
+    from typing_extensions import TypeGuard
+
+    from bentoml._internal.service.openapi.specification import OpenAPISpecification
+
+    # Type aliases for Service class fields
+    ServiceEnvs = t.List[BentoEnvSchema]
+    ServiceImportStr = t.Optional[str]
+
+    def is_service_attributes(obj: t.Any) -> TypeGuard[ServiceAttributes[t.Any]]:
+        """"""Type guard for checking if an object has expected Service attributes.""""""
+        return all(
+            hasattr(obj, attr)
+            for attr in (
+                ""__name__"",
+                ""__doc__"",
+                ""__bentoml_mounted_apps__"",
+                ""__bentoml_gradio_apps__"",
+                ""__call__"",
+            )
+        )
 
-logger = logging.getLogger(""bentoml.io"")
+    # Runtime attribute types for Service class
+    class ServiceAttributes(t.Protocol[T]):
+        """"""Protocol defining expected attributes of Service inner class.""""""
+
+        __name__: str
+        __doc__: t.Optional[str]
+        __bentoml_mounted_apps__: t.List[t.Any]
+        __bentoml_gradio_apps__: t.List[t.Any]
+        __call__: t.Callable[[], T]
+
+
+if t.TYPE_CHECKING:
+    pass
 
-T = t.TypeVar(""T"", bound=object)
-P = t.ParamSpec(""P"")
-R = t.TypeVar(""R"")
+logger = logging.getLogger(""bentoml.io"")
 
 ServiceDecorator: TypeAlias = t.Callable[[type[T]], ""Service[T]""]
 
 
 def with_config(
-    func: t.Callable[t.Concatenate[""Service[t.Any]"", P], R],
-) -> t.Callable[t.Concatenate[""Service[t.Any]"", P], R]:
-    def wrapper(self: Service[t.Any], *args: P.args, **kwargs: P.kwargs) -> R:
+    func: t.Callable[..., t.Any],
+) -> t.Callable[..., t.Any]:
+    def wrapper(self: Service[t.Any], *args: t.Any, **kwargs: t.Any) -> t.Any:
         self.inject_config()
         return func(self, *args, **kwargs)
 
@@ -63,40 +103,123 @@ def convert_envs(envs: t.List[t.Dict[str, t.Any]]) -> t.List[BentoEnvSchema]:
     return [BentoEnvSchema(**env) for env in envs]
 
 
-@attrs.define
+@define(auto_attribs=True, slots=False, frozen=False, eq=False)  # type: ignore[misc]
 class Service(t.Generic[T]):
     """"""A Bentoml service that can be served by BentoML server.""""""
 
-    config: Config
-    inner: type[T]
-    image: t.Optional[Image] = None
-    envs: list[BentoEnvSchema] = attrs.field(factory=list, converter=convert_envs)
-    bento: t.Optional[Bento] = attrs.field(init=False, default=None)
-    models: list[Model[t.Any]] = attrs.field(factory=list)
-    apis: dict[str, APIMethod[t.Any, t.Any]] = attrs.field(factory=dict)
-    dependencies: dict[str, Dependency[t.Any]] = attrs.field(factory=dict, init=False)
-    openapi_service_overrides: dict[str, t.Any] = attrs.field(factory=dict, init=True)
-    mount_apps: list[tuple[ext.ASGIApp, str, str]] = attrs.field(
-        factory=list, init=False
+    config: t.Dict[str, t.Any] = field(
+        factory=dict,
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""ServiceConfig""},
+    )
+    inner: t.Type[T] = field(
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""type[T]""},
+    )
+    image: t.Optional[Image] = field(
+        default=None,
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""ServiceImage""},
+    )
+    envs: t.List[BentoEnvSchema] = field(
+        factory=list,
+        converter=convert_envs,
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""List[BentoEnvSchema]""},
+    )
+    bento: t.Optional[Bento] = field(
+        init=False,
+        default=None,
+        repr=False,
+        eq=False,
+        metadata={""type"": ""ServiceBento""},
+    )
+    models: t.List[t.Union[StoredModel, Model[t.Any]]] = field(
+        factory=list,
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""ModelList""},
     )
-    middlewares: list[tuple[type[ext.AsgiMiddleware], dict[str, t.Any]]] = attrs.field(
-        factory=list, init=False
+    apis: t.Dict[str, APIMethod[..., t.Any]] = field(
+        factory=dict,
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""APIMethodDict""},
+    )
+    dependencies: t.Dict[str, DependencyInstance] = field(
+        factory=dict,
+        init=False,
+        repr=False,
+        eq=False,
+        metadata={""type"": ""DependencyDict""},
+    )
+    openapi_service_overrides: t.Dict[str, t.Any] = field(
+        factory=dict,
+        init=True,
+        repr=True,
+        eq=False,
+        metadata={""type"": ""ComponentDict""},
+    )
+    mount_apps: t.List[t.Tuple[ext.ASGIApp, str, str]] = field(
+        factory=list,
+        init=False,
+        repr=False,
+        eq=False,
+        metadata={""type"": ""MountAppList""},
+    )
+    middlewares: t.List[t.Tuple[t.Type[ext.AsgiMiddleware], t.Dict[str, t.Any]]] = (
+        field(
+            factory=list,
+            init=False,
+            repr=False,
+            eq=False,
+            metadata={""type"": ""MiddlewareList""},
+        )
     )
     # service context
-    context: ServiceContext = attrs.field(init=False, factory=ServiceContext)
-    working_dir: str = attrs.field(init=False, factory=os.getcwd)
+    context: ServiceContext = field(
+        init=False,
+        factory=ServiceContext,
+        eq=False,
+        metadata={""type"": ""ServiceContext""},
+    )
+    working_dir: str = field(
+        init=False,
+        factory=os.getcwd,
+        eq=False,
+        metadata={""type"": ""str""},
+    )
     # import info
-    _caller_module: str = attrs.field(init=False)
-    _import_str: str | None = attrs.field(init=False, default=None)
+    _caller_module: str = field(
+        init=False,
+        default="""",
+        eq=False,
+        metadata={""type"": ""str""},
+    )
+    _import_str: t.Optional[str] = field(
+        init=False,
+        default=None,
+        eq=False,
+        metadata={""type"": ""typing.Optional[str]""},
+    )
 
     def __attrs_post_init__(self) -> None:
-        from .dependency import Dependency
-
         has_task = False
-        for field in dir(self.inner):
-            value = getattr(self.inner, field)
-            if isinstance(value, Dependency):
-                self.dependencies[field] = value
+        inner_attrs = t.cast(ServiceAttributes[T], self.inner)
+        for attr_name in dir(inner_attrs):
+            value = getattr(inner_attrs, attr_name)
+            if isinstance(value, DependencyInstance):
+                self.dependencies[attr_name] = value
             elif isinstance(value, StoredModel):
                 logger.warning(
                     ""`bentoml.models.get()` as the class attribute is not recommended because it requires the model""
@@ -108,7 +231,7 @@ def __attrs_post_init__(self) -> None:
             elif isinstance(value, APIMethod):
                 if value.is_task:
                     has_task = True
-                self.apis[field] = t.cast(""APIMethod[..., t.Any]"", value)
+                self.apis[attr_name] = t.cast(""APIMethod[..., t.Any]"", value)
 
         if has_task:
             traffic = self.config.setdefault(""traffic"", {})
@@ -119,10 +242,10 @@ def __attrs_post_init__(self) -> None:
         if ""openapi_service_overrides"" in self.config:
             self.openapi_service_overrides = self.config[""openapi_service_overrides""]
 
-        pre_mount_apps = getattr(self.inner, ""__bentoml_mounted_apps__"", [])
+        pre_mount_apps = getattr(inner_attrs, ""__bentoml_mounted_apps__"", [])
         if pre_mount_apps:
             self.mount_apps.extend(pre_mount_apps)
-            delattr(self.inner, ""__bentoml_mounted_apps__"")
+            delattr(inner_attrs, ""__bentoml_mounted_apps__"")
 
     def __hash__(self):
         return hash(self.name)
@@ -144,7 +267,7 @@ def __repr__(self) -> str:
         return f""<{self.__class__.__name__} name={self.name!r}>""
 
     @lru_cache
-    def find_dependent_by_path(self, path: str) -> Service[t.Any]:
+    def find_dependent_by_path(self, path: str) -> ""Service[t.Any]"":
         """"""Find a service by path""""""
         attr_name, _, path = path.partition(""."")
         if attr_name not in self.dependencies:
@@ -157,9 +280,9 @@ def find_dependent_by_path(self, path: str) -> Service[t.Any]:
             raise BentoMLException(f""Service {attr_name} not found"")
         if path:
             return dependent.on.find_dependent_by_path(path)
-        return dependent
+        return dependent.on
 
-    def find_dependent_by_name(self, name: str) -> Service[t.Any]:
+    def find_dependent_by_name(self, name: str) -> ""Service[t.Any]"":
         """"""Find a service by name""""""
         try:
             return self.all_services()[name]
@@ -169,23 +292,25 @@ def find_dependent_by_name(self, name: str) -> Service[t.Any]:
     @property
     def url(self) -> str | None:
         """"""Get the URL of the service, or None if the service is not served""""""
-        dependency_map = BentoMLContainer.remote_runner_mapping.get()
+        dependency_map = t.cast(
+            dict[str, str], BentoMLContainer.remote_runner_mapping.get()
+        )
         url = dependency_map.get(self.name)
-        return url.replace(""tcp://"", ""http://"") if url else None
+        return url.replace(""tcp://"", ""http://"") if url is not None else None
 
     @lru_cache(maxsize=1)
-    def all_services(self) -> dict[str, Service[t.Any]]:
+    def all_services(self) -> dict[str, ""Service[t.Any]""]:
         """"""Get a map of the service and all recursive dependencies""""""
-        services: dict[str, Service[t.Any]] = {self.name: self}
+        services: dict[str, ""Service[t.Any]""] = {self.name: self}
         for dependency in self.dependencies.values():
             if dependency.on is None:
                 continue
-            dependents = dependency.on.all_services()
-            conflict = next(
+            dependents: dict[str, ""Service[t.Any]""] = dependency.on.all_services()
+            conflict: str | None = next(
                 (
-                    k
-                    for k in dependents
-                    if k in services and dependents[k] is not services[k]
+                    str(k)
+                    for k, v in dependents.items()
+                    if k in services and v is not services[k]
                 ),
                 None,
             )
@@ -284,7 +409,8 @@ def add_asgi_middleware(
         self.middlewares.append((middleware_cls, options))
 
     def gradio_app_startup_hook(self, max_concurrency: int):
-        gradio_apps = getattr(self.inner, ""__bentoml_gradio_apps__"", [])
+        inner_attrs = t.cast(ServiceAttributes[T], self.inner)
+        gradio_apps = getattr(inner_attrs, ""__bentoml_gradio_apps__"", [])
         if gradio_apps:
             for gradio_app, path, _ in gradio_apps:
                 logger.info(f""Initializing gradio app at: {path or '/'}"")
@@ -296,14 +422,17 @@ def gradio_app_startup_hook(self, max_concurrency: int):
                 else:
                     # gradio >= 5.0
                     blocks.run_startup_events()
-            delattr(self.inner, ""__bentoml_gradio_apps__"")
+            delattr(inner_attrs, ""__bentoml_gradio_apps__"")
 
-    def __call__(self) -> T:
+    def __call__(self) -> t.Union[T, ServiceInstance]:
         try:
             instance = self.inner()
-            instance.to_async = _AsyncWrapper(instance, self.apis.keys())
-            instance.to_sync = _SyncWrapper(instance, self.apis.keys())
-            return instance
+            # Cast to Any to avoid type checking issues with dynamic attribute assignment
+            instance_any = t.cast(t.Any, instance)
+            api_keys = list(self.apis.keys())
+            instance_any.to_async = _AsyncWrapper(instance, api_keys)
+            instance_any.to_sync = _SyncWrapper(instance, api_keys)
+            return t.cast(t.Union[T, ServiceInstance], instance)
         except Exception:
             logger.exception(""Initializing service error"")
             raise
@@ -356,20 +485,20 @@ def serve_http(
         self,
         *,
         working_dir: str | None = None,
-        port: int = Provide[BentoMLContainer.http.port],
-        host: str = Provide[BentoMLContainer.http.host],
-        backlog: int = Provide[BentoMLContainer.api_server_config.backlog],
+        port: int = provide[BentoMLContainer.http.port],
+        host: str = provide[BentoMLContainer.http.host],
+        backlog: int = provide[BentoMLContainer.api_server_config.backlog],
         timeout: int | None = None,
-        ssl_certfile: str | None = Provide[BentoMLContainer.ssl.certfile],
-        ssl_keyfile: str | None = Provide[BentoMLContainer.ssl.keyfile],
-        ssl_keyfile_password: str | None = Provide[
+        ssl_certfile: str | None = provide[BentoMLContainer.ssl.certfile],
+        ssl_keyfile: str | None = provide[BentoMLContainer.ssl.keyfile],
+        ssl_keyfile_password: str | None = provide[
             BentoMLContainer.ssl.keyfile_password
         ],
-        ssl_version: int | None = Provide[BentoMLContainer.ssl.version],
-        ssl_cert_reqs: int | None = Provide[BentoMLContainer.ssl.cert_reqs],
-        ssl_ca_certs: str | None = Provide[BentoMLContainer.ssl.ca_certs],
-        ssl_ciphers: str | None = Provide[BentoMLContainer.ssl.ciphers],
-        bentoml_home: str = Provide[BentoMLContainer.bentoml_home],
+        ssl_version: int | None = provide[BentoMLContainer.ssl.version],
+        ssl_cert_reqs: int | None = provide[BentoMLContainer.ssl.cert_reqs],
+        ssl_ca_certs: str | None = provide[BentoMLContainer.ssl.ca_certs],
+        ssl_ciphers: str | None = provide[BentoMLContainer.ssl.ciphers],
+        bentoml_home: str = provide[BentoMLContainer.bentoml_home],
         development_mode: bool = False,
         reload: bool = False,
         threaded: bool = False,
@@ -575,7 +704,7 @@ async def wrapped_gen(
             return wrapped_gen
         else:
 
-            async def wrapped(*args: P.args, **kwargs: P.kwargs) -> t.Any:
+            async def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> t.Any:
                 return await anyio.to_thread.run_sync(partial(func, **kwargs), *args)
 
             return wrapped
@@ -613,7 +742,7 @@ def wrapped_gen(
             return wrapped_gen
         else:
 
-            def wrapped(*args: P.args, **kwargs: P.kwargs) -> t.Any:
+            def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> t.Any:
                 loop = asyncio.get_event_loop()
                 return loop.run_until_complete(func(*args, **kwargs))
 