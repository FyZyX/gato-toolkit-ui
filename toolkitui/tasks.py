import asyncio

import gato.service
from .executor import app


def run_task(task):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(task())
    finally:
        loop.close()

    return result


async def generate_scenario(service: gato.service.GatoService):
    params = service.create_scenario_parameters()
    prompt = service.create_scenario_prompt(params)
    return await service.create_scenario(prompt)


@app.task
def generate_scenario_task(service: gato.service.GatoService):
    return run_task(generate_scenario(service))
