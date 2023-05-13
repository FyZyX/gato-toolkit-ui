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

## Design and Architecture

See our [design doc](docs/DESIGN.md) for details.

## Contributing

Contributions to the GATO Toolkit UI are welcome! Please read our [contributing guidelines](docs/CONTRIBUTING.md) and [code of conduct](docs/CODE-OF-CONDUCT.md) before you start.

## License

[MIT](https://choosealicense.com/licenses/mit/)
