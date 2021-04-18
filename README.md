# koop

## Requirements
* Python >= 3.9
* Docker >= 20.10
* docker-compose >= 1.29
* Make
* (useful in BE development) poetry >= 1.1.5


## Setup
1. Create a `.env` file in the main project directory:
    ```dotenv
    SECRET_KEY=CHANGE_ME
    DEBUG=True

    POSTGRES_DB=koop
    POSTGRES_USER=koop
    POSTGRES_PASSWORD=CHANGE_ME
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ```
2. Before first running the project:
    ```shell
    docker-compose build
    ```
3. Start the project:
    ```shell
    docker-compose up
    ```

## Development
We use:
* [black](https://black.readthedocs.io/en/stable/) for Python code formatting,
* [prettier](https://prettier.io/) for front-end code formatting,
* [ESlint](https://eslint.org/) for enforcing JS code quality rules.

All these are added as [pre-commit](https://pre-commit.com/) hooks.
Before you start committing, install pre-commit in your local environment and
activate the hooks.

pre-commit is one of the dev-dependencies of the project, so if you use poetry
for local development, just run:
```shell
poetry install
```
Then activate the hooks:
```shell
pre-commit install
```

Although it is not enforced by a pre-commit hook, it is strongly recommended
to use type annotations and often run [mypy](https://mypy.readthedocs.io/) over
the backend code (the containers have to be running for the make command to work):
```shell
make mypy
# or, when you're in the `backend/` directory:
make -C .. mypy
```

### Tests
We use Django's unit test framework, at least for now. The following command
executes `./manage.py test` in the backend container (so the containers have
to be running):
```shell
make test
# or, when you're in the `backend/` directory:
make -C .. test
```
