@@ -78,7 +78,7 @@ async def reduce_dimensionality(
             reduced_embeddings = umap_reducer.fit_transform(embeddings)
             reduced_embeddings = np.asarray(reduced_embeddings)  # Ensure it's an NDArray
             logger.info(
-                f""UMAP dimensionality reduction completed: {embeddings.shape} -> {reduced_embeddings.shape}""
+                f""UMAP dimensionality reduction completed: {embeddings.shape} -> {reduced_embeddings.shape}""  # type: ignore
             )
         except Exception as e:
             logger.error(f""UMAP dimensionality reduction failed: {e}"")