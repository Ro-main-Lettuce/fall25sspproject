@@ -5,6 +5,7 @@
 
 class EchoTextHandler(dingtalk_stream.ChatbotHandler):
     def __init__(self, client):
+        super().__init__()  # Call parent class initializer to set up logger
         self.msg_id = ''
         self.incoming_message = None
         self.client = client  # 用于更新 DingTalkClient 中的 incoming_message