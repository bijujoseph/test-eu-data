import os
import shutil
from pathlib import Path

import yaml
from pydash import strings


class Config:

    def __init__(self):
        super().__init__()
        with open(os.path.join(FileUtils.get_root(), "config.yml"), 'r') as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)

    def get_value(cls, dict, key):
        v = dict
        for p in strings.split(key, "."):
            if v is None: continue
            v = v.get(p)
        return v

    def get(self, key):
        return self.get_value(self._config, key)


class FileUtils:

    @classmethod
    def get_root(cls):
        path = Path(__file__)
        return path.parent.parent

    @classmethod
    def absolute_path(cls, folder, file_name=None):
        if not (file_name is None):
            return cls.get_root().joinpath(folder).joinpath(file_name)
        return cls.get_root().joinpath(folder)

    @classmethod
    def rmdir(cls, path):
        shutil.rmtree(path, ignore_errors=True)

    @classmethod
    def mkdirs(cls, path):
        Path(path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def read_file(cls, file_name):
        with open(file_name, 'r') as f:
            content = f.read()
        return content

    @classmethod
    def write_file(cls, file_name, content, mode="w"):
        with open(file_name, mode) as f:
            f.write(content)
        return file_name

    @classmethod
    def delete_file(cls, file_name):
        Path(file_name).unlink()

    @classmethod
    def list(cls, folder, ext="*.json"):
        return list(Path(folder).rglob(ext))

    @classmethod
    def copy(cls, src, dest, mode="w"):
        cls.write_file(dest, cls.read_file(src), mode)
