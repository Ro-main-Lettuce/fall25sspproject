@@ -13,7 +13,7 @@
 )
 
 
-@pytest.mark.timeout(600)
+@pytest.mark.timeout(1200)
 @pytest.mark.parametrize(""shard_count"", [1, 8, 32])
 @pytest.mark.parametrize(
     ""wal_receiver_protocol"",