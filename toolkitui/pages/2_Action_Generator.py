import os
import pathlib

import celery.result
import gato.entity
import gato.service
import streamlit

from toolkitui import executor, storage


def schedule_action_tasks(
        api_key: str,
        scenarios: list[gato.entity.Scenario],
) -> list[celery.result.AsyncResult]:
    num_actions = len(scenarios)
    progress_text = f"Generating {num_actions} actions. Please wait."
    my_bar = streamlit.progress(0, text=progress_text)

    action_tasks = []
    with streamlit.spinner():
        for k, scenario in enumerate(scenarios):
            task = executor.generate_action_task.delay(api_key)
            action_tasks.append(task)
            progress = (k + 1) / num_actions
            if progress == 1:
                progress_text = f"COMPLETE: Generated {num_actions} actions."
            else:
                progress_text = f"Generated {k + 1} of {num_actions} actions." \
                                f" Please wait."
            my_bar.progress((k + 1) / num_actions, text=progress_text)
    return action_tasks


def render_action(action: gato.entity.Action, container):
    container.write(action.description)
    container.write(f"Action ID: {action.id}")
    container.divider()


def render_action_generator():
    streamlit.header("Generate Actions")
    api_key = streamlit.text_input("OpenAI API Key", os.environ.get("OPENAI_API_KEY"))
    base_path = pathlib.Path(__file__).parent.parent.parent
    path = base_path / pathlib.Path("data/actions")
    complete_scenarios = {f.name.replace("action", "scenario") for f in path.iterdir()}
    path = base_path / pathlib.Path("data/scenarios")
    all_scenarios = {f.name for f in path.iterdir()}
    all_scenarios -= complete_scenarios
    all_scenarios = [storage.load_scenario(s.removesuffix(".yml"))
                     for s in all_scenarios]
    options = [s.id for s in all_scenarios]
    choices = streamlit.multiselect("Scenarios", options=options, default=options[:2])

    if streamlit.button("Generate Actions"):
        scenarios = list(filter(lambda s: s.id in choices, all_scenarios))
        action_tasks = schedule_action_tasks(api_key, scenarios)

        container = streamlit.container()
        done = 0
        with streamlit.spinner():
            while done < len(scenarios):
                for task in action_tasks:
                    if not task.ready():
                        continue
                    scenario = task.get()
                    storage.save_scenario(scenario)
                    render_action(scenario, container)
                    done += 1


def main():
    render_action_generator()


if __name__ == '__main__':
    main()
