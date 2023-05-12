import os

import gato.entity
import gato.llm
import gato.service
import streamlit

from toolkitui import storage


def render_scenarios(service: gato.service.GatoService, num_scenarios: int):
    progress_text = f"Generating {num_scenarios} scenarios. Please wait."
    my_bar = streamlit.progress(0, text=progress_text)
    container = streamlit.container()

    with streamlit.spinner():
        for k in range(num_scenarios):
            params = service.create_scenario_parameters()
            prompt = service.create_scenario_prompt(params)
            scenario = service.create_scenario(prompt)
            storage.save_scenario(scenario)
            progress = (k + 1) / num_scenarios
            if progress == 1:
                progress_text = f"COMPLETE: Generated {num_scenarios} scenarios."
            else:
                progress_text = f"Generated {k + 1} of {num_scenarios} scenario." \
                                f" Please wait."
            my_bar.progress((k + 1) / num_scenarios, text=progress_text)
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
        render_scenarios(service, num_scenarios)


def main():
    render_scenario_generator()


if __name__ == '__main__':
    main()
