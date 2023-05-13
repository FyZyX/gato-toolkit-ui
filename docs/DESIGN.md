# Design and Architecture

The RLHI Data Generator is composed of several key components:

1. [Streamlit UI](https://streamlit.io): This is the primary interface that users interact with. It allows users to input their OpenAI API key, specify the number of scenarios and actions to generate, and view the generated results.
2. [Gato Toolkit](https://github.com/FyZyX/gato-toolkit): This is the core library used for generating scenarios and potential actions. It utilizes the language models provided by services like the OpenAI API.
3. [Celery Task Queue](https://celeryproject.org): In order to handle parallel generation of multiple scenarios and actions, the application uses Celery, a powerful asynchronous task queue/job queue based on distributed message passing.
4. [Redis](https://redis.io): This serves two roles. It acts as the message broker for Celery, handling communication between the main application and the worker processes. Additionally, it serves as a simple in-memory database for storing generated scenarios and actions.
5. [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose): The application and its components are containerized using Docker, and orchestrated using Docker Compose. This simplifies deployment and ensures a consistent environment for running the application.

This architecture allows the RLHI Data Generator to efficiently generate a large number of scenarios and actions in parallel, and handle user interaction in a responsive manner.

For a more detailed view of the application's architecture, please refer to the `docker-compose.yml` file in the repository.

## Docker and Docker Compose

Data storage is achieved via Redis, which is given a volume mount in Docker Compose so that data persists between sessions.
This storage option is very limited, and our current solution for relationships between data is very hacky.

The point of this storage system right now is to ensure that any work done by the API is at leased saved for later use.
As the application grows, we will likely move rapidly to a more structured database, but deciding on schema must come first.
Redis is good place ot store this unstructured data for now, while development is still early.
