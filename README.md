# koop

## Requirements
* Python >= 3.9
* Docker >= 20.10
* docker-compose >= 1.29
* Make
* (useful in BE development) poetry >= 1.1.5


## Setup
1. Create a `.env` file in the main project directory:
    ```
    SECRET_KEY=CHANGE_ME
    DEBUG=True

    POSTGRES_DB=koop
    POSTGRES_USER=koop
    POSTGRES_PASSWORD=CHANGE_ME
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ```
2. Before first running the project:
    ```
    docker-compose build
    ```
3. Start the project:
    ```
    docker-compose up
    ```
