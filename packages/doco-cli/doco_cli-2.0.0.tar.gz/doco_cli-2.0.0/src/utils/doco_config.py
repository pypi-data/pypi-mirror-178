import os
import typing as t

import pydantic
import tomli

from src.utils.rsync import RsyncConfig


class TextSubstitutions(pydantic.BaseModel):
    pattern: str
    replace: str


class DocoConfigTextSubstitutions(pydantic.BaseModel):
    bind_mount_volume_path: list[TextSubstitutions] = []


class DocoOutputConfig(pydantic.BaseModel):
    text_substitutions: DocoConfigTextSubstitutions = DocoConfigTextSubstitutions()


class DocoBackupConfig(pydantic.BaseModel):
    rsync: RsyncConfig = RsyncConfig()


class DocoConfig(pydantic.BaseModel):
    output: DocoOutputConfig = DocoOutputConfig()
    backup: DocoBackupConfig = DocoBackupConfig()


def _load_config_from_filesystem(project_path: str) -> t.Optional[DocoConfig]:
    root = os.path.abspath(project_path)
    toml_file_name = "doco.config.toml"
    json_file_name = "doco.config.json"
    while True:
        path = os.path.join(root, toml_file_name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                return DocoConfig.parse_obj(tomli.load(f))

        path = os.path.join(root, json_file_name)
        if os.path.isfile(path):
            return DocoConfig.parse_file(path)

        if root == "/":
            break
        root = os.path.dirname(root)
    return None


def _load_backup_rsync_config_from_env(config: RsyncConfig) -> None:
    prefix = "DOCO_BACKUP_RSYNC_"
    config.rsh = os.environ.get(f"{prefix}RSH", config.rsh)
    config.host = os.environ.get(f"{prefix}HOST", config.host)
    config.user = os.environ.get(f"{prefix}USER", config.user)
    config.module = os.environ.get(f"{prefix}MODULE", config.module)
    config.root = os.environ.get(f"{prefix}ROOT", config.root)


def load_doco_config(project_path: str) -> DocoConfig:
    config = _load_config_from_filesystem(project_path)
    if config is None:
        config = DocoConfig()
    _load_backup_rsync_config_from_env(config.backup.rsync)
    return config
