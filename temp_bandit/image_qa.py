@@ -3,12 +3,10 @@
 # SPDX-License-Identifier: Apache-2.0
 import os
 
-from PIL import Image
+from ......coding.func_with_reqs import with_requirements
 
-from autogen.coding.func_with_reqs import with_requirements
 
-
-@with_requirements([""transformers"", ""torch""], [""transformers"", ""torch"", ""PIL"", ""os""])
+@with_requirements([""transformers"", ""torch"", ""PIL""], [""transformers"", ""torch"", ""os""])
 def image_qa(image, question, ckpt=""Salesforce/blip-vqa-base""):
     """"""Perform question answering on an image using a pre-trained VQA model.
 
@@ -20,6 +18,7 @@ def image_qa(image, question, ckpt=""Salesforce/blip-vqa-base""):
         dict: The generated answer text.
     """"""
     import torch
+    from PIL import Image
     from transformers import BlipForQuestionAnswering, BlipProcessor
 
     def image_processing(img):