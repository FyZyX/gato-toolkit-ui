import gato.entity
import streamlit

from toolkitui import storage


def render_scenario(scenario: gato.entity.Scenario, container):
    container.write(scenario.description)
    container.write(f"Scenario ID: {scenario.id}")
    container.divider()


def render_action(
        scenario: gato.entity.Scenario,
        action: gato.entity.Action,
        container
):
    container.header(scenario.id)
    container.subheader("Scenario")
    container.write(scenario.description)
    container.subheader("Action")
    container.write(action.description)
    container.divider()


def main():
    tabs = streamlit.tabs(["Scenarios", "Actions"])

    with tabs[0]:
        streamlit.subheader("View Scenarios")
        keys = storage.list_scenarios()
        selected_keys = streamlit.multiselect("Scenarios", options=keys)
        container = streamlit.container()

        for key in selected_keys:
            scenario = storage.load_scenario(key)
            render_scenario(scenario, container)

    with tabs[1]:
        streamlit.subheader("View Actions")
        keys = storage.list_actions()
        action_keys = streamlit.multiselect("Actions", options=keys)
        scenario_keys = [key.replace("action", "scenario") for key in action_keys]
        container = streamlit.container()

        for scenario_key, action_key in zip(scenario_keys, action_keys):
            scenario = storage.load_scenario(scenario_key)
            action = storage.load_action(action_key)
            render_action(scenario, action, container)


if __name__ == '__main__':
    main()
