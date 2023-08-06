import os
import yaml
from typing import List
from .models import Settings, Session, Schema, Group
from rich import print

settings_file_location = os.path.expanduser('~/.ssh/pfm2.settings.yaml')
# settings = {
#     'show_schema_link': 'false',
#     'wait_after_start': 0.5,
#     'wait_after_stop': 0.5,
#     'table_border': 'false',
#     'show_pid': 'false',
#     'schemas': [],
#     'groups': []
# }
_settings: Settings
_schemas: List[Schema] = []
_groups: List[Group] = []


def settings():
    return _settings


def load_settings():
    global _settings, _schemas, _groups, settings_file_location
    # print("Load settings")

    if not os.path.isfile(settings_file_location):
        save_settings()

    with open(settings_file_location, "r") as stream:
        try:
            loaded_settings = yaml.load(stream, Loader=yaml.BaseLoader)
            # print(loaded_settings)
            _settings = Settings(**loaded_settings)
            _schemas = _settings.schemas
            _groups = _settings.groups
            # settings.update(loaded_settings)

            #if loaded_settings != settings:
            #    save_settings()
        except yaml.YAMLError as exc:
            print(exc)


def save_settings():
    global _settings, settings_file_location

    print(f"[b]Updating configuration file on '{settings_file_location}'[/b]")

    with open(settings_file_location, "w") as stream:
        try:
            yaml.dump(_settings.dict(), stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_schemas_ids():
    result = []
    for schema in _settings.schemas:
        result.append(schema.id)

    return result


def get_schemas():
    return _settings.schemas


def set_ports_active(ports):
    _settings.ports_active = ports


def get_ports_active():
    return _settings.ports_active


def get_schema(schema_id) -> Schema:
    # print(f"Looking for {schema_id}")
    for schema in _settings.schemas:
        if schema.id == schema_id:
            return schema

    raise Exception(f"Schema {schema_id} not found")

