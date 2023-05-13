import gato.entity
import streamlit

from toolkitui import storage


def render_scenario(scenario: gato.entity.Scenario, container):
    container.write(scenario.description)
    container.write(f"Scenario ID: {scenario.id}")
    container.divider()


def main():
    keys = storage.list_scenarios()
    selected_keys = streamlit.multiselect("Scenarios", options=keys)
    container = streamlit.container()

    for key in selected_keys:
        scenario = storage.load_scenario(key)
        render_scenario(scenario, container)


if __name__ == '__main__':
    main()
