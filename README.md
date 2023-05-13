# GATO Toolkit UI

## Overview

This project is meant to expose the functionality from the [GATO Toolkit](https://github.com/FyZyX/gato-toolkit) in a simple user interface.
These datasets contain scenarios and potential actions that an AI model might take, and are created using an LLM and a specific set of prompt engineering techniques.

## Features

- Generation of unique scenarios and potential actions.
- Parallel generation for speed using a Celery task queue.
- Storage of generated scenarios and actions using Redis.

## Prerequisites

- Docker

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Run Docker Compose.
4. The application should now be running at `http://localhost:8501`.

```shell
git clone <repo_url>
cd gato-toolkit-ui
docker-compose up -d
```

## Usage

### Scenario Generator

1. Input your OpenAI API key.
2. Input the number of scenarios you'd like to generate.
3. Click `Generate Scenarios` to start the generation process. The generated scenarios will be displayed on the screen, and also stored in the database.

### Action Generator

1. Input your OpenAI API key.
2. Select the scenarios for which you'd like to generate actions. Only scenarios that do not yet have actions generated can be selected (known limitation).
3. Click `Generate Actions` to start the generation process. The generated actions will be displayed on the screen, and also stored in the database.

## Architecture

The RLHI Data Generator is composed of several key components:

1. [Streamlit UI](https://streamlit.io): This is the primary interface that users interact with. It allows users to input their OpenAI API key, specify the number of scenarios and actions to generate, and view the generated results.
2. [Gato Toolkit](https://github.com/FyZyX/gato-toolkit): This is the core library used for generating scenarios and potential actions. It utilizes the language models provided by services like the OpenAI API.
3. [Celery Task Queue](https://celeryproject.org): In order to handle parallel generation of multiple scenarios and actions, the application uses Celery, a powerful asynchronous task queue/job queue based on distributed message passing.
4. [Redis](https://redis.io): This serves two roles. It acts as the message broker for Celery, handling communication between the main application and the worker processes. Additionally, it serves as a simple in-memory database for storing generated scenarios and actions.
5. [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose): The application and its components are containerized using Docker, and orchestrated using Docker Compose. This simplifies deployment and ensures a consistent environment for running the application.

This architecture allows the RLHI Data Generator to efficiently generate a large number of scenarios and actions in parallel, and handle user interaction in a responsive manner.

For a more detailed view of the application's architecture, please refer to the `docker-compose.yml` file in the repository.

## Contributing

Contributions to the RLHI Data Generator are welcome! Please read our [contributing guidelines](docs/CONTRIBUTING.md) and [code of conduct](docs/CODE-OF-CONDUCT.md) before you start.

## License

[MIT](https://choosealicense.com/licenses/mit/)
