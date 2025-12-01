@@ -131,6 +131,7 @@ async def run_e2e(prompt: str, standalone: bool, with_edit=True):
                     # Clean up Docker containers
                     stop_docker_compose(temp_dir, container_names[""project_name""])
 
+@pytest.mark.skipif(os.getenv(""GEMINI_API_KEY"") is None, reason=""GEMINI_API_KEY is not set"")
 async def test_e2e_generation():
     await run_e2e(standalone=False, prompt=DEFAULT_APP_REQUEST)
 