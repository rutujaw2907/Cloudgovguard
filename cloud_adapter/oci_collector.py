import oci

class OCICollector:
    def __init__(self):
        self.config = oci.config.from_file()

        # Root tenancy (needed for IAM)
        self.tenancy_id = self.config["tenancy"]

        # Your given compartment
        self.compartment_id = "ocid1.compartment.oc1..aaaaaaaaanzjjmrj2prg7k62ipouc7wf4fchj3dkc7p6lgfc2qlqlzuceoia"

        # Clients
        self.identity = oci.identity.IdentityClient(self.config)
        self.network = oci.core.VirtualNetworkClient(self.config)
        self.object_storage = oci.object_storage.ObjectStorageClient(self.config)

    # ---------------- IAM ----------------

    def get_users(self):
        return self.identity.list_users(
            compartment_id=self.tenancy_id
        ).data

    def get_policies(self):
        return self.identity.list_policies(
            compartment_id=self.tenancy_id
        ).data

    # ---------------- NETWORK ----------------

    def get_vcns(self):
        return self.network.list_vcns(
            compartment_id=self.compartment_id
        ).data

    def get_security_lists(self):
        security_lists = []

        vcns = self.get_vcns()

        for vcn in vcns:
            sls = self.network.list_security_lists(
                compartment_id=self.compartment_id,
                vcn_id=vcn.id
            ).data

            security_lists.extend(sls)

        return security_lists

    # ---------------- STORAGE ----------------

    def get_buckets(self):
        namespace = self.object_storage.get_namespace().data

        return self.object_storage.list_buckets(
            namespace_name=namespace,
            compartment_id=self.compartment_id
        ).data

    # ---------------- MASTER FUNCTION ----------------

    def collect_all(self):
        return {
            "users": self.get_users(),
            "policies": self.get_policies(),
            "security_lists": self.get_security_lists(),
            "buckets": self.get_buckets()
        }