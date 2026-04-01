import oci


class OCICollector:
    def __init__(self):
        self.config = oci.config.from_file()
        self.tenancy_id = self.config["tenancy"]

        self.identity = oci.identity.IdentityClient(self.config)
        self.network = oci.core.VirtualNetworkClient(self.config)
        self.object_storage = oci.object_storage.ObjectStorageClient(self.config)

    def get_users(self):
        return self.identity.list_users(compartment_id=self.tenancy_id).data

    def get_policies(self):
        return self.identity.list_policies(compartment_id=self.tenancy_id).data

    def get_compartments(self):
        compartments = self.identity.list_compartments(
            compartment_id=self.tenancy_id,
            compartment_id_in_subtree=True,
            access_level="ANY"
        ).data

        root = type("RootCompartment", (), {
            "id": self.tenancy_id,
            "name": "root"
        })()

        return [root] + compartments

    def get_security_lists(self):
        security_lists = []
        compartments = self.get_compartments()

        for comp in compartments:
            try:
                vcns = self.network.list_vcns(compartment_id=comp.id).data
                for vcn in vcns:
                    sls = self.network.list_security_lists(compartment_id=comp.id, vcn_id=vcn.id).data
                    security_lists.extend(sls)
            except Exception as e:
                print(f"[WARN] Failed fetching security lists for compartment {comp.name}: {e}")

        return security_lists

    def get_buckets(self):
        buckets = []
        namespace = self.object_storage.get_namespace().data
        compartments = self.get_compartments()

        for comp in compartments:
            try:
                result = self.object_storage.list_buckets(
                    namespace_name=namespace,
                    compartment_id=comp.id
                ).data
                buckets.extend(result)
            except Exception as e:
                print(f"[WARN] Failed fetching buckets for compartment {comp.name}: {e}")

        return buckets

    def collect_all(self):
        return {
            "users": self.get_users(),
            "policies": self.get_policies(),
            "security_lists": self.get_security_lists(),
            "buckets": self.get_buckets()
        }