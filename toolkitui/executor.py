import asyncio
import os

import gato.llm
import gato.service
from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

app = Celery('tasks', broker=broker_url, backend=result_backend)

app.conf.update(
    task_serializer='json',
    accept_content=['json', 'pickle'],
    result_serializer='pickle',
    timezone='America/Los_Angeles',
    enable_utc=True,
)


def run_task(task, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(task(*args, **kwargs))
    finally:
        loop.close()

    return result


async def generate_scenario(api_key: str):
    model = gato.llm.LLM(api_key)
    service = gato.service.GatoService(model)
    params = service.create_scenario_parameters()
    prompt = service.create_scenario_prompt(params)
    return await service.create_scenario(prompt)


@app.task
def generate_scenario_task(api_key: str):
    return run_task(generate_scenario, api_key)


if __name__ == '__main__':
    app.start()
