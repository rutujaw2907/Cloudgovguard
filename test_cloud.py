from cloud_adapter.oci_collector import OCICollector
from normalizer.resource_parser import normalize_all

collector = OCICollector()

print("Collecting data from OCI...")
raw = collector.collect_all()

print("Normalizing...")
resources = normalize_all(raw)

print(f"Total resources: {len(resources)}")

for r in resources[:10]:
    print(r)