@@ -203,7 +203,7 @@ def main():
         sys.exit(0 if success else 1)
 
     else:
-        print(json.dumps(cdk_info, indent=2))
+        print(json.dumps(cdk_info))
 
 
 if __name__ == ""__main__"":