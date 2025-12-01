@@ -43,7 +43,7 @@ async def completion(
             thinking_tokens=0,
         )
 
-
+@pytest.mark.skipif(os.getenv(""GEMINI_API_KEY"") is None, reason=""GEMINI_API_KEY is not set"")
 async def test_cached_llm():
     with tempfile.NamedTemporaryFile(delete_on_close=False) as tmp_file:
         base_llm = StubLLM()
@@ -70,6 +70,7 @@ async def test_cached_llm():
 
 
 
+@pytest.mark.skipif(os.getenv(""GEMINI_API_KEY"") is None, reason=""GEMINI_API_KEY is not set"")
 async def test_cached_lru():
     with tempfile.NamedTemporaryFile(delete_on_close=False) as tmp_file:
         base_llm = StubLLM()
@@ -112,6 +113,7 @@ async def test_cached_lru():
         assert json.dumps(new_resp.to_dict()) != responses[""first""], ""First request should not hit the cache""
         assert base_llm.calls == 4, ""Base LLM should still be called four times""
 
+@pytest.mark.skipif(os.getenv(""GEMINI_API_KEY"") is None, reason=""GEMINI_API_KEY is not set"")
 async def test_gemini():
     client = get_llm_client(model_name=""gemini-flash"")
     resp = await client.completion(
@@ -126,6 +128,7 @@ async def test_gemini():
             raise ValueError(f""Unexpected content type: {type(text)}"")
 
 
+@pytest.mark.skipif(os.getenv(""GEMINI_API_KEY"") is None, reason=""GEMINI_API_KEY is not set"")
 async def test_gemini_with_image():
     client = get_llm_client(model_name=""gemini-flash-lite"")
     image_path = os.path.join(