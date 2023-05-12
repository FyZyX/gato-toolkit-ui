import pathlib

import yaml

import gato.entity


def save_scenario(scenario: gato.entity.Scenario):
    with open(pathlib.Path("../data/scenarios")) as file:
        yaml.safe_dump(scenario.dict(), file)
