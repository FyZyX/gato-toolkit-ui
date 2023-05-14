import os

import gato.entity
import gato.service
import streamlit
import celery.result

from toolkitui import executor, storage


def schedule_scenario_tasks(
        api_key: str, num_scenarios: int
) -> list[celery.result.AsyncResult]:
    with streamlit.spinner():
        return [executor.generate_scenario_task.delay(api_key)
                for _ in range(num_scenarios)]


def render_scenario(scenario: gato.entity.Scenario, container):
    container.write(scenario.description)
    container.write(f"Scenario ID: {scenario.id}")
    container.divider()


def get_complete_tasks(tasks):
    return (task for task in tasks if task.ready())


def update_progress(progress_bar, complete, total):
    if complete == total:
        progress_text = f"Completed all {total} tasks."
    else:
        progress_text = f"Completed {complete} of {total} " \
                        f"tasks. Please wait."
    progress_bar.progress(complete / total, text=progress_text)


def render_scenario_generator():
    streamlit.header("Generate Scenarios")
    api_key = os.environ.get("OPENAI_API_KEY")
    api_key = streamlit.text_input("OpenAI API Key", value=api_key, type="password")
    num_scenarios = streamlit.number_input(
        "Number of scenarios to generate",
        min_value=1, value=1,
    )
    if streamlit.button("Generate Scenarios"):
        scenario_tasks = schedule_scenario_tasks(api_key, num_scenarios)

        progress_text = f"Waiting for {num_scenarios} tasks. Please wait."
        progress_bar = streamlit.progress(0, text=progress_text)
        container = streamlit.container()
        complete = 0
        with streamlit.spinner():
            while complete < num_scenarios:
                for task in get_complete_tasks(scenario_tasks):
                    scenario = task.get()
                    storage.save_scenario(scenario)
                    scenario_tasks.remove(task)
                    render_scenario(scenario, container)
                    complete += 1
                    update_progress(progress_bar, complete, num_scenarios)


def main():
    render_scenario_generator()


if __name__ == '__main__':
    main()
