@@ -5,8 +5,8 @@
 
 from bespokelabs.curator import LLM
 
-# python tests/batch/simple_batch.py --log-level DEBUG --n-requests 3 --batch-size 1 --batch-check-interval 10 --model gpt-4o-mini
-# python tests/batch/simple_batch.py --log-level DEBUG --n-requests 3 --batch-size 1 --batch-check-interval 10 --model claude-3-5-haiku-20241022
+# python tests/batch/simple_batch.py --log-level DEBUG --n-requests 3 --batch-size 1 --batch-check-interval 10 --model gpt-4o-mini # type: ignore
+# python tests/batch/simple_batch.py --log-level DEBUG --n-requests 3 --batch-size 1 --batch-check-interval 10 --model claude-3-5-haiku-20241022 # type: ignore
 
 
 def main(args):