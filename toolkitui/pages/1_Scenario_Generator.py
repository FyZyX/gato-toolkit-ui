import os

import gato.entity
import gato.llm
import gato.service
import streamlit
import celery.result

from .. import tasks


def schedule_scenario_tasks(
        service: gato.service.GatoService, num_scenarios: int
) -> list[celery.result.AsyncResult]:
    progress_text = f"Scheduling {num_scenarios} scenarios. Please wait."
    my_bar = streamlit.progress(0, text=progress_text)
    scenario_tasks = []

    for k in range(num_scenarios):
        task = tasks.generate_scenario_task.delay(service)
        scenario_tasks.append(task)
        progress = (k + 1) / num_scenarios
        if progress == 1:
            progress_text = f"Scheduled {num_scenarios} scenarios."
        else:
            progress_text = f"Scheduled {k + 1} of {num_scenarios} scenario." \
                            f" Please wait."
        my_bar.progress((k + 1) / num_scenarios, text=progress_text)
    return scenario_tasks


def render_scenario(scenario: gato.entity.Scenario, container):
    container.write(scenario.description)
    container.write(f"Scenario ID: {scenario.id}")
    container.divider()


def render_scenario_generator():
    streamlit.header("Generate Scenarios")
    api_key = streamlit.text_input("OpenAI API Key", os.environ.get("OPENAI_API_KEY"))
    num_scenarios = streamlit.number_input(
        "Number of scenarios to generate",
        min_value=1, value=1,
    )
    if streamlit.button("Generate Scenarios"):
        model = gato.llm.LLM(api_key)
        service = gato.service.GatoService(model)
        scenario_tasks = schedule_scenario_tasks(service, num_scenarios)

        container = streamlit.container()
        done = 0
        with streamlit.spinner():
            while done < num_scenarios:
                for task in scenario_tasks:
                    if not task.ready():
                        continue
                    scenario = task.get()
                    render_scenario(scenario, container)
                    done += 1


def main():
    render_scenario_generator()


if __name__ == '__main__':
    main()
