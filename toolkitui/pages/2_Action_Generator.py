import json
import os

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
    progress_text = f"Scheduling {num_actions} actions. Please wait."
    my_bar = streamlit.progress(0, text=progress_text)

    action_tasks = []
    with streamlit.spinner():
        for k, scenario in enumerate(scenarios):
            task = executor.generate_action_task.delay(
                api_key, json.loads(scenario.json()),
            )
            action_tasks.append(task)
            progress = (k + 1) / num_actions
            if progress == 1:
                progress_text = f"Scheduled {num_actions} actions."
            else:
                progress_text = f"Scheduled {k + 1} of {num_actions} actions." \
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
    action_keys = storage.list_actions()
    complete_scenarios = {key.replace("action", "scenario") for key in action_keys}
    all_scenarios = set(storage.list_scenarios())
    all_scenarios -= complete_scenarios
    all_scenarios = [storage.load_scenario(s) for s in all_scenarios]
    options = [s.id for s in all_scenarios]
    choices = streamlit.multiselect("Scenarios", options=options, default=options[:2])

    if streamlit.button("Generate Actions"):
        scenarios = list(filter(lambda s: s.id in choices, all_scenarios))
        action_tasks = schedule_action_tasks(api_key, scenarios)

        container = streamlit.container()
        done = 0
        with streamlit.spinner():
            while done < len(scenarios):
                for k, task in enumerate(action_tasks):
                    if not task.ready():
                        continue
                    action = task.get()
                    scenario = scenarios[k]
                    storage.save_action(scenario, action)
                    action_tasks.remove(task)
                    render_action(action, container)
                    done += 1


def main():
    render_action_generator()


if __name__ == '__main__':
    main()
