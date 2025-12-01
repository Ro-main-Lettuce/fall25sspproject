@@ -2,42 +2,32 @@
 #
 # SPDX-License-Identifier: Apache-2.0
 
+from dataclasses import dataclass
 from logging import Logger, getLogger
 from typing import Any, Callable, Optional, TypeVar, Union
 
-import anyio
-from asyncer import asyncify, create_task_group, syncify
-from fastapi import WebSocket
+from anyio import lowlevel
+from asyncer import create_task_group
 
 from ...tools import Tool
-from .. import SwarmAgent
-from ..agent import Agent
-from ..contrib.swarm_agent import AfterWorkOption, initiate_swarm_chat
-from ..conversable_agent import ConversableAgent
+from .clients.realtime_client import RealtimeClientProtocol, get_client
 from .function_observer import FunctionObserver
-from .oai_realtime_client import OpenAIRealtimeClient, OpenAIRealtimeWebRTCClient, Role
-from .realtime_client import RealtimeClientProtocol
 from .realtime_observer import RealtimeObserver
 
 F = TypeVar(""F"", bound=Callable[..., Any])
 
 global_logger = getLogger(__name__)
 
-SWARM_SYSTEM_MESSAGE = (
-    ""You are a helpful voice assistant. Your task is to listen to user and to coordinate the tasks based on his/her inputs.""
-    ""You can and will communicate using audio output only.""
-)
 
-QUESTION_ROLE: Role = ""user""
-QUESTION_MESSAGE = (
-    ""I have a question/information for myself. DO NOT ANSWER YOURSELF, GET THE ANSWER FROM ME. ""
-    ""repeat the question to me **WITH AUDIO OUTPUT** and AFTER YOU GET THE ANSWER FROM ME call 'answer_task_question'

""
-    ""The question is: '{}'

""
-)
-QUESTION_TIMEOUT_SECONDS = 20
+@dataclass
+class RealtimeAgentCallbacks:
+    """"""Callbacks for the Realtime Agent.""""""
 
+    # async empty placeholder function
+    on_observers_ready: Callable[[], Any] = lambda: lowlevel.checkpoint()
 
-class RealtimeAgent(ConversableAgent):
+
+class RealtimeAgent:
     """"""(Experimental) Agent for interacting with the Realtime Clients.""""""
 
     def __init__(
@@ -47,9 +37,8 @@ def __init__(
         audio_adapter: Optional[RealtimeObserver] = None,
         system_message: str = ""You are a helpful AI Assistant."",
         llm_config: dict[str, Any],
-        voice: str = ""alloy"",
         logger: Optional[Logger] = None,
-        websocket: Optional[WebSocket] = None,
+        **client_kwargs: Any,
     ):
         """"""(Experimental) Agent for interacting with the Realtime Clients.
 
@@ -58,59 +47,29 @@ def __init__(
             audio_adapter (Optional[RealtimeObserver] = None): The audio adapter for the agent.
             system_message (str): The system message for the agent.
             llm_config (dict[str, Any], bool): The config for the agent.
-            voice (str): The voice for the agent.
-            websocket (Optional[WebSocket] = None): WebSocket from WebRTC javascript client
+            logger (Optional[Logger]): The logger for the agent.
+            **client_kwargs (Any): The keyword arguments for the client.
         """"""
-        super().__init__(
-            name=name,
-            is_termination_msg=None,
-            max_consecutive_auto_reply=None,
-            human_input_mode=""ALWAYS"",
-            function_map=None,
-            code_execution_config=False,
-            # no LLM config is passed down to the ConversableAgent
-            llm_config=False,
-            default_auto_reply="""",
-            description=None,
-            chat_messages=None,
-            silent=None,
-            context_variables=None,
-        )
         self._logger = logger
-        self._function_observer = FunctionObserver(logger=logger)
-        self._audio_adapter = audio_adapter
-        self._realtime_client: RealtimeClientProtocol = OpenAIRealtimeClient(
-            llm_config=llm_config, voice=voice, system_message=system_message, logger=logger
-        )
-        if websocket is not None:
-            self._realtime_client = OpenAIRealtimeWebRTCClient(
-                llm_config=llm_config, voice=voice, system_message=system_message, websocket=websocket, logger=logger
-            )
-
-        self._voice = voice
+        self._name = name
+        self._system_message = system_message
 
-        self._observers: list[RealtimeObserver] = [self._function_observer]
-        if self._audio_adapter:
-            # audio adapter is not needed for WebRTC
-            self._observers.append(self._audio_adapter)
+        self._realtime_client: RealtimeClientProtocol = get_client(
+            llm_config=llm_config, logger=self.logger, **client_kwargs
+        )
 
         self._registred_realtime_tools: dict[str, Tool] = {}
+        self._observers: list[RealtimeObserver] = [FunctionObserver(logger=logger)]
 
-        # is this all Swarm related?
-        self._oai_system_message = [{""content"": system_message, ""role"": ""system""}]  # todo still needed? see below
-        self.register_reply(
-            [Agent, None], RealtimeAgent.check_termination_and_human_reply, remove_other_reply_funcs=True
-        )
+        if audio_adapter:
+            self._observers.append(audio_adapter)
 
-        self._answer_event: anyio.Event = anyio.Event()
-        self._answer: str = """"
-        self._start_swarm_chat = False
-        self._initial_agent: Optional[SwarmAgent] = None
-        self._agents: Optional[list[SwarmAgent]] = None
+        self.callbacks = RealtimeAgentCallbacks()
 
-    def _validate_name(self, name: str) -> None:
-        # RealtimeAgent does not need to validate the name
-        pass
+    @property
+    def system_message(self) -> str:
+        """"""Get the system message for the agent.""""""
+        return self._system_message
 
     @property
     def logger(self) -> Logger:
@@ -135,60 +94,25 @@ def register_observer(self, observer: RealtimeObserver) -> None:
         """"""
         self._observers.append(observer)
 
-    def register_swarm(
-        self,
-        *,
-        initial_agent: SwarmAgent,
-        agents: list[SwarmAgent],
-        system_message: Optional[str] = None,
-    ) -> None:
-        """"""Register a swarm of agents with the Realtime Agent.
+    async def start_observers(self) -> None:
+        for observer in self._observers:
+            self._tg.soonify(observer.run)(self)
 
-        Args:
-            initial_agent (SwarmAgent): The initial agent.
-            agents (list[SwarmAgent]): The agents in the swarm.
-            system_message (str): The system message for the agent.
-        """"""
-        logger = self.logger
-        if not system_message:
-            if self.system_message != ""You are a helpful AI Assistant."":
-                logger.warning(
-                    ""Overriding system message set up in `__init__`, please use `system_message` parameter of the `register_swarm` function instead.""
-                )
-            system_message = SWARM_SYSTEM_MESSAGE
-
-        self._oai_system_message = [{""content"": system_message, ""role"": ""system""}]
-
-        self._start_swarm_chat = True
-        self._initial_agent = initial_agent
-        self._agents = agents
-
-        self.register_realtime_function(name=""answer_task_question"", description=""Answer question from the task"")(
-            self.set_answer
-        )
+        # wait for the observers to be ready
+        for observer in self._observers:
+            await observer.wait_for_ready()
+
+        await self.callbacks.on_observers_ready()
 
     async def run(self) -> None:
         """"""Run the agent.""""""
         # everything is run in the same task group to enable easy cancellation using self._tg.cancel_scope.cancel()
         async with create_task_group() as self._tg:
             # connect with the client first (establishes a connection and initializes a session)
             async with self._realtime_client.connect():
-                # start the observers
-                for observer in self._observers:
-                    self._tg.soonify(observer.run)(self)
-
-                # wait for the observers to be ready
-                for observer in self._observers:
-                    await observer.wait_for_ready()
-
-                if self._start_swarm_chat and self._initial_agent and self._agents:
-                    self._tg.soonify(asyncify(initiate_swarm_chat))(
-                        initial_agent=self._initial_agent,
-                        agents=self._agents,
-                        user_agent=self,  # type: ignore[arg-type]
-                        messages=""Find out what the user wants."",
-                        after_work=AfterWorkOption.REVERT_TO_USER,
-                    )
+                # start the observers and wait for them to be ready
+                await self.realtime_client.session_update(session_options={""instructions"": self.system_message})
+                await self.start_observers()
 
                 # iterate over the events
                 async for event in self.realtime_client.read_events():
@@ -227,71 +151,3 @@ def _decorator(func_or_tool: Union[F, Tool]) -> Tool:
             return tool
 
         return _decorator
-
-    def reset_answer(self) -> None:
-        """"""Reset the answer event.""""""
-        self._answer_event = anyio.Event()
-
-    def set_answer(self, answer: str) -> str:
-        """"""Set the answer to the question.""""""
-        self._answer = answer
-        self._answer_event.set()
-        return ""Answer set successfully.""
-
-    async def get_answer(self) -> str:
-        """"""Get the answer to the question.""""""
-        await self._answer_event.wait()
-        return self._answer
-
-    async def ask_question(self, question: str, question_timeout: int) -> None:
-        """"""Send a question for the user to the agent and wait for the answer.
-        If the answer is not received within the timeout, the question is repeated.
-
-        Args:
-            question: The question to ask the user.
-            question_timeout: The time in seconds to wait for the answer.
-        """"""
-        self.reset_answer()
-        await self._realtime_client.send_text(role=QUESTION_ROLE, text=question)
-
-        async def _check_event_set(timeout: int = question_timeout) -> bool:
-            for _ in range(timeout):
-                if self._answer_event.is_set():
-                    return True
-                await anyio.sleep(1)
-            return False
-
-        while not await _check_event_set():
-            await self._realtime_client.send_text(role=QUESTION_ROLE, text=question)
-
-    def check_termination_and_human_reply(
-        self,
-        messages: Optional[list[dict[str, Any]]] = None,
-        sender: Optional[Agent] = None,
-        config: Optional[Any] = None,
-    ) -> tuple[bool, Union[str, None]]:
-        """"""Check if the conversation should be terminated and if the agent should reply.
-
-        Called when its agents turn in the chat conversation.
-
-        Args:
-            messages: list of dict
-                the messages in the conversation
-            sender: Agent
-                the agent sending the message
-            config: any
-                the config for the agent
-        """"""
-        if not messages:
-            return False, None
-
-        async def get_input() -> None:
-            async with create_task_group() as tg:
-                tg.soonify(self.ask_question)(
-                    QUESTION_MESSAGE.format(messages[-1][""content""]),
-                    question_timeout=QUESTION_TIMEOUT_SECONDS,
-                )
-
-        syncify(get_input)()
-
-        return True, {""role"": ""user"", ""content"": self._answer}  # type: ignore[return-value]