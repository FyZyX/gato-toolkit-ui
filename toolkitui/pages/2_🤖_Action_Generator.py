import json
import os
import time

import celery.result
import gato.entity
import gato.service
import streamlit

from toolkitui import executor, storage


def schedule_tasks(
        api_key: str,
        scenarios: list[gato.entity.Scenario],
) -> list[celery.result.AsyncResult]:
    return [executor.generate_action_task.delay(
        api_key, json.loads(scenario.json()),
    ) for k, scenario in enumerate(scenarios)]


def render_action(action: gato.entity.Action, container):
    container.write(action.description)
    container.write(f"Action ID: {action.id}")
    container.divider()


def update_progress(progress_bar, done, total):
    if done == total:
        progress_text = f"Completed all {total} tasks."
    else:
        progress_text = f"Completed {done} of {total} " \
                        f"tasks. Please wait."
    progress_bar.progress(done / total, text=progress_text)


def get_complete_tasks(tasks):
    return (task for task in tasks if task.ready())


def wait_for_results(progress_bar, tasks):
    total, complete = len(tasks), 0
    while complete < total:
        for task in get_complete_tasks(tasks):
            result = task.get()
            tasks.remove(task)
            complete += 1
            update_progress(progress_bar, complete, total)
            yield result
            time.sleep(0.1)


def render_action_generator():
    streamlit.header("Generate Actions")
    api_key = os.environ.get("OPENAI_API_KEY")
    api_key = streamlit.text_input("OpenAI API Key", value=api_key, type="password")
    action_keys = storage.list_actions()
    complete_scenarios = {key.replace("action", "scenario") for key in action_keys}
    all_scenarios = set(storage.list_scenarios())
    all_scenarios -= complete_scenarios
    all_scenarios = [storage.load_scenario(s) for s in all_scenarios]
    options = [s.id for s in all_scenarios]
    choices = streamlit.multiselect("Scenarios", options=options, default=options[:2])

    if streamlit.button("Generate Actions"):
        scenarios = list(filter(lambda s: s.id in choices, all_scenarios))
        with streamlit.spinner():
            action_tasks = schedule_tasks(api_key, scenarios)

        num_actions = len(action_tasks)
        progress_text = f"Waiting for {num_actions} tasks. Please wait."
        progress_bar = streamlit.progress(0, text=progress_text)
        container = streamlit.container()
        with streamlit.spinner():
            for k, action in enumerate(wait_for_results(progress_bar, action_tasks)):
                scenario = scenarios[k]
                storage.save_action(scenario, action)
                render_action(action, container)


def main():
    render_action_generator()


if __name__ == '__main__':
    main()
