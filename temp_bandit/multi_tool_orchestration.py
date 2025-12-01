@@ -15,22 +15,25 @@
 from tqdm.auto import tqdm
 from pandas import DataFrame
 from datasets import load_dataset
-import random
-import string
+
+# Note: random and string imports removed as we're using an existing index
 from openai import OpenAI
 import agentops
 from pinecone import Pinecone
-from pinecone import ServerlessSpec
 
 load_dotenv()
 
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 os.environ[""PINECONE_API_KEY""] = os.getenv(""PINECONE_API_KEY"", ""your_pinecone_api_key_here"")
 
-agentops.init(auto_start_session=True)
+agentops.init(
+    auto_start_session=False,
+    trace_name=""OpenAI Multi-Tool Orchestration"",
+    tags=[""openai"", ""multi-tool"", ""agentops-example""],
+)
 tracer = agentops.start_trace(
-    trace_name=""Multi-Tool Orchestration with RAG"",
+    trace_name=""OpenAI Multi-Tool Orchestration with RAG"",
     tags=[""multi-tool-orchestration-rag-demo"", ""openai-responses"", ""agentops-example""],
 )
 client = OpenAI()
@@ -46,58 +49,60 @@
 )
 print(""Example merged text:"", ds_dataframe[""merged""].iloc[0])
 
-# ### Create a Pinecone Index Based on the Dataset
-# Use the dataset itself to determine the embedding dimensionality. For example, compute one embedding from the merged column and then create the index accordingly.
+# ### Connect to Existing Pinecone Index
+# We'll connect to an existing Pinecone index instead of creating a new one. We still compute an embedding to ensure compatibility with the existing index dimensions.
 MODEL = ""text-embedding-3-small""  # Replace with your production embedding model if needed
 
 # Compute an embedding for the first document to obtain the embedding dimension.
+# This helps ensure compatibility with the existing index dimensions.
 sample_embedding_resp = client.embeddings.create(input=[ds_dataframe[""merged""].iloc[0]], model=MODEL)
 embed_dim = len(sample_embedding_resp.data[0].embedding)
 print(f""Embedding dimension: {embed_dim}"")
 
 # Initialize Pinecone using your API key.
 pc = Pinecone(api_key=os.environ[""PINECONE_API_KEY""])
 
-# Define the Pinecone serverless specification.
-AWS_REGION = ""us-east-1""
-spec = ServerlessSpec(cloud=""aws"", region=AWS_REGION)
-
-# Create a random index name with lower case alphanumeric characters and '-'
-index_name = ""pinecone-index-"" + """".join(random.choices(string.ascii_lowercase + string.digits, k=10))
+# Use the existing Pinecone index
+index_name = ""pinecone-index-btimakzhfe""
 
-# Create the index if it doesn't already exist.
-if index_name not in pc.list_indexes().names():
-    pc.create_index(index_name, dimension=embed_dim, metric=""dotproduct"", spec=spec)
-
-# Connect to the index.
+# Connect to the existing index (no need to create it as it already exists)
 index = pc.Index(index_name)
 time.sleep(1)
-print(""Index stats:"", index.describe_index_stats())
+index_stats = index.describe_index_stats()
+print(""Index stats:"", index_stats)
 
-# #### Upsert the Dataset into Pinecone index
+# #### Check if the index already has data, and optionally upsert new data
 #
-# Process the dataset in batches, generate embeddings for each merged text, prepare metadata (including separate Question and Answer fields), and upsert each batch into the index. You may also update metadata for specific entries if needed.
-batch_size = 32
-for i in tqdm(range(0, len(ds_dataframe[""merged""]), batch_size), desc=""Upserting to Pinecone""):
-    i_end = min(i + batch_size, len(ds_dataframe[""merged""]))
-    lines_batch = ds_dataframe[""merged""][i:i_end]
-    ids_batch = [str(n) for n in range(i, i_end)]
-
-    # Create embeddings for the current batch.
-    res = client.embeddings.create(input=[line for line in lines_batch], model=MODEL)
-    embeds = [record.embedding for record in res.data]
-
-    # Prepare metadata by extracting original Question and Answer.
-    meta = []
-    for record in ds_dataframe.iloc[i:i_end].to_dict(""records""):
-        q_text = record[""Question""]
-        a_text = record[""Response""]
-        # Optionally update metadata for specific entries.
-        meta.append({""Question"": q_text, ""Answer"": a_text})
-
-    # Upsert the batch into Pinecone.
-    vectors = list(zip(ids_batch, embeds, meta))
-    index.upsert(vectors=vectors)
+# Check if the existing index already has sufficient data for our demo.
+# If it has data, we'll use it as-is. If not, we'll add some sample data.
+if index_stats.total_vector_count > 0:
+    print(f""✅ Index already contains {index_stats.total_vector_count} vectors. Using existing data."")
+else:
+    print(""📝 Index is empty. Adding sample data from the medical dataset..."")
+    # Process the dataset in batches, generate embeddings for each merged text, prepare metadata (including separate Question and Answer fields), and upsert each batch into the index. You may also update metadata for specific entries if needed.
+    batch_size = 32
+    for i in tqdm(range(0, len(ds_dataframe[""merged""]), batch_size), desc=""Upserting to Pinecone""):
+        i_end = min(i + batch_size, len(ds_dataframe[""merged""]))
+        lines_batch = ds_dataframe[""merged""][i:i_end]
+        ids_batch = [str(n) for n in range(i, i_end)]
+
+        # Create embeddings for the current batch.
+        res = client.embeddings.create(input=[line for line in lines_batch], model=MODEL)
+        embeds = [record.embedding for record in res.data]
+
+        # Prepare metadata by extracting original Question and Answer.
+        meta = []
+        for record in ds_dataframe.iloc[i:i_end].to_dict(""records""):
+            q_text = record[""Question""]
+            a_text = record[""Response""]
+            # Optionally update metadata for specific entries.
+            meta.append({""Question"": q_text, ""Answer"": a_text})
+
+        # Upsert the batch into Pinecone.
+        vectors = list(zip(ids_batch, embeds, meta))
+        index.upsert(vectors=vectors)
+
+    print(""✅ Data upserting completed."")
 
 
 # ### Query the Pinecone Index
@@ -342,4 +347,15 @@ def query_pinecone_index(client, index, model, query_text):
 print(response_2.output_text)
 agentops.end_trace(tracer, end_state=""Success"")
 
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    agentops.validate_trace_spans(trace_context=tracer)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise
+
+
 # Here, we have seen  how to utilize OpenAI's Responses API to implement a Retrieval-Augmented Generation (RAG) approach with multi-tool calling capabilities. It showcases an example where the model selects the appropriate tool based on the input query: general questions may be handled by built-in tools such as web-search, while specific medical inquiries related to internal knowledge are addressed by retrieving context from a vector database (such as Pinecone) via function calls. Additonally, we have showcased how multiple tool calls can be sequentially combined to generate a final response based on our instructions provided to responses API. Happy coding!