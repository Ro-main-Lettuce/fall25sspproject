@@ -82,8 +82,8 @@ def __init__(self, name='bool', on=1., off=0.):
   def __call__(self, t):
     return tf.expand_dims(tf.where(t, self.on, self.off), -1)
 
-  def distance(self, predicted, target):
-    logits = tf.squeeze(predicted, [-1])
+  def distance(self, embedded: tf.Tensor, target: bool):
+    logits = tf.squeeze(embedded, [-1])
     labels = tf.cast(target, float_type)
 
     common_shape = tf.broadcast_static_shape(logits.shape, labels.shape)
@@ -93,11 +93,11 @@ def distance(self, predicted, target):
     return tf.nn.sigmoid_cross_entropy_with_logits(
         logits=logits, labels=labels)
 
-  def sample(self, t, temperature=None):
-    t = tf.squeeze(t, -1)
+  def sample(self, embedded: tf.Tensor, temperature=None):
+    logits = tf.squeeze(embedded, -1)
     if temperature is not None:
-      t = t / temperature
-    dist = tfp.distributions.Bernoulli(logits=t, dtype=tf.bool)
+      logits = logits / temperature
+    dist = tfp.distributions.Bernoulli(logits=logits, dtype=tf.bool)
     return dist.sample()
 
   def distribution(self, embedded: tf.Tensor):
@@ -196,38 +196,6 @@ def sample(self, embedded, temperature=None):
   def distribution(self, embedded: tf.Tensor):
     return tfp.distributions.Categorical(logits=embedded, dtype=self.tf_dtype)
 
-class NullEmbedding(Embedding[In, None]):
-  size = 0
-
-  def from_state(self, state: In) -> None:
-    return None
-
-  def __call__(self, t):
-    assert t is None
-    return None
-
-  def map(self, f, *args: None) -> None:
-    for x in args:
-      assert x is None
-    return None
-
-  def flatten(self, none: None):
-    pass
-
-  def unflatten(self, seq):
-    return None
-
-  def decode(self, out: None) -> None:
-    assert out is None
-    return None
-
-  def dummy(self) -> None:
-    """"""A dummy value.""""""
-    return None
-
-  def sample(self, embedded, **_):
-    return None
-
 NT = TypeVar(""NT"")
 
 class StructEmbedding(Embedding[NT, NT]):
@@ -317,11 +285,11 @@ class SplatKwargs(Generic[T]):
   """"""Wraps a function that takes kwargs.""""""
 
   def __init__(self, f: Callable[..., T], fixed_kwargs: Mapping[str, Any] = {}):
-      self._func = f
-      self._fixed_kwargs = fixed_kwargs
+    self._func = f
+    self._fixed_kwargs = fixed_kwargs
 
   def __call__(self, kwargs: Mapping[str, Any]) -> T:
-      return self._func(**kwargs, **self._fixed_kwargs)
+    return self._func(**kwargs, **self._fixed_kwargs)
 
 def struct_embedding_from_nt(name: str, nt: NT) -> StructEmbedding[NT]:
   return StructEmbedding(
@@ -386,9 +354,9 @@ def make_player_embedding(
     with_speeds: bool = False,
     with_controller: bool = True,
 ) -> StructEmbedding[Player]:
-    embed_xy = FloatEmbedding(""xy"", scale=xy_scale)
+  embed_xy = FloatEmbedding(""xy"", scale=xy_scale)
 
-    embedding = [
+  embedding = [
       (""percent"", FloatEmbedding(""percent"", scale=0.01)),
       (""facing"", BoolEmbedding(""facing"", off=-1.)),
       ('x', embed_xy),
@@ -403,24 +371,24 @@ def make_player_embedding(
       # (""charging_smash"", embedFloat),
       (""shield_strength"", FloatEmbedding(""shield_size"", scale=shield_scale)),
       (""on_ground"", embed_bool),
-    ]
-
-    if with_controller:
-      # TODO: make this configurable
-      embed_controller_default = get_controller_embedding()  # continuous sticks
-      embedding.append(('controller', embed_controller_default))
-
-    if with_speeds:
-      embed_speed = FloatEmbedding(""speed"", scale=speed_scale)
-      embedding.extend([
-          ('speed_air_x_self', embed_speed),
-          ('speed_ground_x_self', embed_speed),
-          ('speed_y_self', embed_speed),
-          ('speed_x_attack', embed_speed),
-          ('speed_y_attack', embed_speed),
-      ])
-
-    return ordered_struct_embedding(""player"", embedding, Player)
+  ]
+
+  if with_controller:
+    # TODO: make this configurable
+    embed_controller_default = get_controller_embedding()  # continuous sticks
+    embedding.append(('controller', embed_controller_default))
+
+  if with_speeds:
+    embed_speed = FloatEmbedding(""speed"", scale=speed_scale)
+    embedding.extend([
+        ('speed_air_x_self', embed_speed),
+        ('speed_ground_x_self', embed_speed),
+        ('speed_y_self', embed_speed),
+        ('speed_x_attack', embed_speed),
+        ('speed_y_attack', embed_speed),
+    ])
+
+  return ordered_struct_embedding(""player"", embedding, Player)
 
 @dataclasses.dataclass
 class PlayerConfig: