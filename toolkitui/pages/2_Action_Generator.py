import os
import pathlib
from typing import Iterable

import gato.entity
import gato.llm
import gato.service
import streamlit

from .. import storage


def render_actions(
        service: gato.service.GatoService,
        scenarios: Iterable[gato.entity.Scenario],
        num_actions: int,
):
    progress_text = f"Generating {num_actions} actions. Please wait."
    my_bar = streamlit.progress(0, text=progress_text)
    container = streamlit.container()

    with streamlit.spinner():
        for k, scenario in enumerate(scenarios):
            prompt = service.create_action_prompt(scenario)
            action = service.create_action(prompt)
            storage.save_action(scenario, action)
            progress = (k + 1) / num_actions
            if progress == 1:
                progress_text = f"COMPLETE: Generated {num_actions} actions."
            else:
                progress_text = f"Generated {k + 1} of {num_actions} actions." \
                                f" Please wait."
            my_bar.progress((k + 1) / num_actions, text=progress_text)
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
        model = gato.llm.LLM(api_key)
        scenarios = list(filter(lambda s: s.id in choices, all_scenarios))
        service = gato.service.GatoService(model)
        render_actions(service, scenarios, len(scenarios))


def main():
    render_action_generator()


if __name__ == '__main__':
    main()
