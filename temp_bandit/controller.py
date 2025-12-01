@@ -51,11 +51,10 @@ async def _process_query(selected_query: entities.Query):
                             # find pipeline
                             # Here firstly find the bot, then find the pipeline, in case the bot adapter's config is not the latest one.
                             # Like aiocqhttp, once a client is connected, even the adapter was updated and restarted, the existing client connection will not be affected.
-                            bot = await self.ap.platform_mgr.get_bot_by_uuid(selected_query.bot_uuid)
-                            if bot:
-                                pipeline = await self.ap.pipeline_mgr.get_pipeline_by_uuid(
-                                    bot.bot_entity.use_pipeline_uuid
-                                )
+                            pipeline_uuid = selected_query.pipeline_uuid
+
+                            if pipeline_uuid:
+                                pipeline = await self.ap.pipeline_mgr.get_pipeline_by_uuid(pipeline_uuid)
                                 if pipeline:
                                     await pipeline.run(selected_query)
 