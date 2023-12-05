# Hera

## Setup
<!-- ### Python Environment
1. Setup `python` virtual environment.
    ```
    python3 -m venv venv
    ```
    > **Warning** <br />
    > The environment must be named `venv` since it will be mounted onto the container orchestrated by `docker-compose.dev.yml`.
2. Activate the environment.
- Linux
    ```
    source venv/bin/activate
    ```
3. Install dependencies.
    ```
    pip install -r ./requirements.txt
    ``` -->

### Docker
1. Build `hera-app`
    ```
    docker compose up -f docker-compose.dev.yml build
    ```
    This will build a dev image for the flask app.
    > **Note** <br />
    > This developer container cluster can handle live changes to the flask app.
    But, if there are any changes to the dependency requirements, the image must
    be build again.

## Running
<!-- 1. Activate the python virtual environment (`venv`). -->
1. Execute `docker compose -f docker-compose.dev.yml up`
