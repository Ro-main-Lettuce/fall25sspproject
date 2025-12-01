from datasets import load_dataset

ds = load_dataset("hao-li/AIDev")

print(ds)
print("\nAvailable keys:")
print(list(ds.keys()))

print("\nColumn names per split:")
for key in ds.keys():
    print(f"\n=== {key} ===")
    print(ds[key].column_names)

