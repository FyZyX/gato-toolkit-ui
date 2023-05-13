import gato.entity
import streamlit

from toolkitui import storage


def render_action(
        scenario: gato.entity.Scenario,
        action: gato.entity.Action,
        container
):
    container.subheader(f"Scenario")
    container.write(scenario.description)
    container.subheader(f"Action")
    container.write(action.description)
    container.divider()


def main():
    keys = storage.list_actions()
    action_keys = streamlit.multiselect("Actions", options=keys)
    scenario_keys = [key.replace("action", "scenario") for key in keys]
    container = streamlit.container()

    for scenario_key, action_key in zip(scenario_keys, action_keys):
        scenario = storage.load_scenario(scenario_key)
        action = storage.load_action(action_key)
        render_action(scenario, action, container)


if __name__ == '__main__':
    main()
