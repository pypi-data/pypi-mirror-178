
class VolumeMount:
    def __init__(self, mount_path: str = None,
                 mount_propagation: str = None,
                 name: str = None,
                 read_only: bool = None,
                 sub_path: str = None,
                 sub_path_expr: str = None):

        self.mount_path = mount_path
        self.mount_propagation = mount_propagation
        self.name = name
        self.read_only = read_only
        self.sub_path = sub_path
        self.sub_path_expr = sub_path_expr
