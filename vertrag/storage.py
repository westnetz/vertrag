import os.path
import yaml

from pathlib import Path

class FileStore:
    """
    Backend Class to handle files. This base class provides
    methods for their childs, to access data in the filesystem.
    """

    key = ""
    file_prefix = None

    def __init__(self, file_dir, cwd):
        self.cwd = Path(cwd)
        self.file_dir = file_dir

    def _get_filename(self, file_id, ext=None):
        if self.file_prefix:
            file_id = "{}_{}".format(self.file_prefix, file_id)
        if ext:
            return "{}.{}".format(file_id, ext)
        else:
            return file_id

    def _get_fullpath(self, file_id, ext=None):
        return os.path.join(
            self.cwd,
            self.file_dir,
            self._get_filename(file_id, ext)
        )

class YamlStore(FileStore):

    def __getitem__(self, file_id):
        with open(self._get_fullpath(file_id, "yaml")) as yaml_file:
            return yaml.safe_load(yaml_file)

    def __setitem__(self, file_id, data):
        with open(self._get_fullpath(file_id, "yaml"), "x") as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))

class OrdersStore(YamlStore):

    key = "orders_dir"
    file_prefix = "order"

class PositionsStore(YamlStore):

    key = "positions_dir"

class ContractsStore(YamlStore):

    key = "contracts_dir"

class AssetsStore(FileStore):

    key = "assets_dir"

    def __getitem__(self, asset_id):
        return self.get_fullpath(asset_id)

class TemplatesStore(FileStore):

    key = "templates_dir"
