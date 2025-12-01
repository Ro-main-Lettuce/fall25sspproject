@@ -84,33 +84,7 @@ async def create_tables(self):
             }
 
             await self.execute_async(sqlalchemy.insert(pipeline.LegacyPipeline).values(pipeline_data))
-        else:
-            default_pipeline_result = await self.execute_async(
-                sqlalchemy.select(pipeline.LegacyPipeline).where(pipeline.LegacyPipeline.is_default == True)
-            )
-            default_pipeline_row = default_pipeline_result.first()
-            if default_pipeline_row:
-                default_pipeline_uuid = default_pipeline_row[0]
-
-        # write default webchat bot
-        from ..entity.persistence import bot as persistence_bot
-        result = await self.execute_async(
-            sqlalchemy.select(persistence_bot.Bot).where(persistence_bot.Bot.adapter == 'webchat')
-        )
-        if result.first() is None:
-            self.ap.logger.info('Creating default webchat bot...')
-
-            bot_data = {
-                'uuid': str(uuid.uuid4()),
-                'name': 'WebChat调试机器人',
-                'description': '用于流水线调试的WebChat适配器机器人',
-                'adapter': 'webchat',
-                'adapter_config': {},
-                'enable': True,
-                'use_pipeline_uuid': default_pipeline_uuid,
-            }
 
-            await self.execute_async(sqlalchemy.insert(persistence_bot.Bot).values(bot_data))
         # =================================
 
         # run migrations