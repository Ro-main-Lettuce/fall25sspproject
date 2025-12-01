@@ -34,7 +34,7 @@ def validate_name(cls, v):
 def test_xai_raw_response_sync(model, mode):
     """"""Test that _raw_response is attached to sync XAI responses""""""
     client = instructor.from_provider(f""xai/{model}"", mode=mode)
-    
+
     user = client.chat.completions.create(
         response_model=User,
         messages=[
@@ -48,7 +48,7 @@ def test_xai_raw_response_sync(model, mode):
             },
         ],
     )
-    
+
     assert isinstance(user, User)
     assert user.name.lower() == ""jason""
     assert user.age == 25
@@ -67,7 +67,7 @@ def test_xai_raw_response_sync(model, mode):
 async def test_xai_raw_response_async(model, mode):
     """"""Test that _raw_response is attached to async XAI responses""""""
     client = instructor.from_provider(f""xai/{model}"", mode=mode, async_client=True)
-    
+
     user = await client.chat.completions.create(
         response_model=User,
         messages=[
@@ -81,7 +81,7 @@ async def test_xai_raw_response_async(model, mode):
             },
         ],
     )
-    
+
     assert isinstance(user, User)
     assert user.name.lower() == ""jason""
     assert user.age == 25
@@ -99,7 +99,7 @@ async def test_xai_raw_response_async(model, mode):
 def test_xai_raw_response_with_validator_sync(model, mode):
     """"""Test that _raw_response works with validated models in sync mode""""""
     client = instructor.from_provider(f""xai/{model}"", mode=mode)
-    
+
     user = client.chat.completions.create(
         response_model=UserValidated,
         max_retries=2,
@@ -114,7 +114,7 @@ def test_xai_raw_response_with_validator_sync(model, mode):
             },
         ],
     )
-    
+
     assert isinstance(user, UserValidated)
     assert user.name == ""JASON""
     assert user.age == 25
@@ -133,7 +133,7 @@ def test_xai_raw_response_with_validator_sync(model, mode):
 async def test_xai_raw_response_with_validator_async(model, mode):
     """"""Test that _raw_response works with validated models in async mode""""""
     client = instructor.from_provider(f""xai/{model}"", mode=mode, async_client=True)
-    
+
     user = await client.chat.completions.create(
         response_model=UserValidated,
         max_retries=2,
@@ -148,7 +148,7 @@ async def test_xai_raw_response_with_validator_async(model, mode):
             },
         ],
     )
-    
+
     assert isinstance(user, UserValidated)
     assert user.name == ""JASON""
     assert user.age == 25
@@ -165,7 +165,7 @@ async def test_xai_raw_response_with_validator_async(model, mode):
 def test_xai_create_with_completion():
     """"""Test that create_with_completion works with XAI provider""""""
     client = instructor.from_provider(""xai/grok-3-mini"", mode=instructor.Mode.XAI_JSON)
-    
+
     user, raw_response = client.chat.completions.create_with_completion(
         response_model=User,
         messages=[
@@ -179,7 +179,7 @@ def test_xai_create_with_completion():
             },
         ],
     )
-    
+
     assert isinstance(user, User)
     assert user.name.lower() == ""jason""
     assert user.age == 25
@@ -197,8 +197,10 @@ def test_xai_create_with_completion():
 )
 async def test_xai_create_with_completion_async():
     """"""Test that create_with_completion works with XAI provider in async mode""""""
-    client = instructor.from_provider(""xai/grok-3-mini"", mode=instructor.Mode.XAI_JSON, async_client=True)
-    
+    client = instructor.from_provider(
+        ""xai/grok-3-mini"", mode=instructor.Mode.XAI_JSON, async_client=True
+    )
+
     user, raw_response = await client.chat.completions.create_with_completion(
         response_model=User,
         messages=[
@@ -212,7 +214,7 @@ async def test_xai_create_with_completion_async():
             },
         ],
     )
-    
+
     assert isinstance(user, User)
     assert user.name.lower() == ""jason""
     assert user.age == 25