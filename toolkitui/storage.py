import pathlib

import yaml

import gato.entity


def save_scenario(scenario: gato.entity.Scenario):
    key = f"scenario_{scenario.id}"
    with open(pathlib.Path(f"../data/scenarios/{key}")) as file:
        yaml.safe_dump(scenario.dict(), file)


def load_scenario(key) -> gato.entity.Scenario:
    with open(pathlib.Path(f"../data/scenarios/{key}")) as file:
        return gato.entity.Scenario(**yaml.safe_load(file))
