@@ -98,6 +98,7 @@ async def get_local_llm_models(address: str | None = None) -> list[dict[str, str
         )
 
         import asyncio
+
         loop = asyncio.get_event_loop()
         response = await loop.run_in_executor(None, client.models.list)
 