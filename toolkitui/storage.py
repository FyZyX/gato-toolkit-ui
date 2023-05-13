import json

import redis

import gato.entity

_REDIS_CLIENT = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


def save_scenario(scenario: gato.entity.Scenario):
    key = f"scenario_{scenario.id}"
    scenario_data = scenario.json()
    _REDIS_CLIENT.set(key, scenario_data)


def load_scenario(key) -> gato.entity.Scenario:
    scenario_data = _REDIS_CLIENT.get(key)
    scenario_dict = json.loads(scenario_data)
    return gato.entity.Scenario(**scenario_dict)


def save_action(scenario: gato.entity.Scenario, action: gato.entity.Action):
    key = f"action_{scenario.id}"
    action_data = action.json()
    _REDIS_CLIENT.set(key, action_data)


def load_action(key) -> gato.entity.Action:
    action_data = _REDIS_CLIENT.get(key)
    action_dict = json.loads(action_data)
    return gato.entity.Action(**action_dict)


def list_scenarios() -> list[str]:
    return _REDIS_CLIENT.keys(pattern="scenario_*")


def list_actions() -> list[str]:
    return _REDIS_CLIENT.keys(pattern="action_*")
