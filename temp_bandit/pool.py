@@ -35,6 +35,7 @@ async def add_query(
         message_event: platform_events.MessageEvent,
         message_chain: platform_message.MessageChain,
         adapter: msadapter.MessagePlatformAdapter,
+        pipeline_uuid: typing.Optional[str] = None,
     ) -> entities.Query:
         async with self.condition:
             query = entities.Query(
@@ -48,6 +49,7 @@ async def add_query(
                 resp_messages=[],
                 resp_message_chain=[],
                 adapter=adapter,
+                pipeline_uuid=pipeline_uuid,
             )
             self.queries.append(query)
             self.query_id_counter += 1