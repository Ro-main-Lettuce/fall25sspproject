@@ -15,7 +15,7 @@
 from openai.types.chat import ChatCompletion
 
 if TYPE_CHECKING:
-    from autogen import Agent, ConversableAgent, OpenAIWrapper
+    from .. import Agent, ConversableAgent, OpenAIWrapper
 
 F = TypeVar(""F"", bound=Callable[..., Any])
 ConfigItem = dict[str, Union[str, list[str]]]