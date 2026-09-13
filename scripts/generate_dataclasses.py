import json
import yaml
import sys

from dataclass_wizard.v0.wizard_cli.schema import PyCodeGenerator


def load_yaml_file(yaml_fname: str):
    data = None
    with open(yaml_fname, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    return data


data = load_yaml_file("files.yml")
print(PyCodeGenerator(json.dumps(data), experimental=True).py_code)
