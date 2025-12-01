@@ -89,7 +89,7 @@ async def test_update_files_endpoint():
 async def test_get_request_endpoint():
     request_id = str(uuid.uuid4())
     subdomain = ""abcd1234""
-    
+
     request_data = {
         ""_id"": request_id,
         ""type"": ""http"",
@@ -100,19 +100,19 @@ async def test_get_request_endpoint():
         ""headers"": {""host"": ""test.com""},
         ""date"": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
     }
-    
+
     mock_redis.get.reset_mock()
     mock_redis.lindex.reset_mock()
-    
+
     mock_redis.get.return_value = ""0""  # Index in the list
-    
+
     mock_redis.lindex.return_value = json.dumps(request_data)
-    
+
     response = client.get(f""/api/get_request?id={request_id}&subdomain={subdomain}"")
-    
+
     assert response.status_code == 200
     assert response.json() == request_data
-    
+
     mock_redis.get.assert_called_with(f""request:{subdomain}:{request_id}"")
     mock_redis.lindex.assert_called_with(f""requests:{subdomain}"", ""0"")
 
@@ -121,25 +121,26 @@ async def test_get_request_endpoint():
 async def test_get_request_invalid_id():
     request_id = ""nonexistent-id""  # Not a valid UUID format
     subdomain = ""abcd1234""
-    
+
     mock_redis.get.reset_mock()
-    
+
     response = client.get(f""/api/get_request?id={request_id}&subdomain={subdomain}"")
-    
+
     assert response.status_code == 404
     assert ""detail"" in response.json()
     assert ""Invalid request ID"" in response.json()[""detail""]
 
+
 @pytest.mark.asyncio
 async def test_get_request_not_found():
     request_id = str(uuid.uuid4())
     subdomain = ""abcd1234""
-    
+
     mock_redis.get.reset_mock()
     mock_redis.get.return_value = None  # Request index not found
-    
+
     response = client.get(f""/api/get_request?id={request_id}&subdomain={subdomain}"")
-    
+
     assert response.status_code == 404
     assert ""detail"" in response.json()
     assert ""Request not found"" in response.json()[""detail""]
@@ -149,7 +150,7 @@ async def test_get_request_not_found():
 async def test_websocket_invalid_token():
     with client.websocket_connect(""/api/ws"") as websocket:
         websocket.send_text(""invalid-token"")
-        
+
         data = websocket.receive_json()
         assert ""cmd"" in data
         assert data[""cmd""] == ""invalid_token""
@@ -165,7 +166,7 @@ async def test_delete_all_endpoint():
         ""subdomain"": ""abcd1234"",
     }
     token = jwt.encode(payload, ""test-secret"", algorithm=""HS256"")
-    
+
     mock_redis.delete.reset_mock()
     mock_redis.delete.return_value = True
     mock_redis.keys.reset_mock()
@@ -176,11 +177,11 @@ async def test_delete_all_endpoint():
     ]
     mock_redis.lrange.reset_mock()
     mock_redis.lrange.return_value = []
-    
+
     with patch(""backend.app.config.jwt_secret"", ""test-secret""):
         response = client.post(""/api/delete_all"", params={""token"": token})
-        
+
         assert response.status_code == 200
         assert response.json() == {""msg"": ""Deleted all requests""}
-        
+
         mock_redis.delete.assert_called()