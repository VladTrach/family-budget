# family-budget
Family budget Django application


## Installation instruction for local development

- Install docker (https://docs.docker.com/engine/install/ubuntu/) and docker-compose (https://docs.docker.com/compose/install/#install-compose-on-linux-systems)
- Copy the `.env-LOCAL` file to a new file `.env` for using and customization environment variables in the project
- Run `docker-compose build`
- Run `docker volume create --name=family-budget-db-data`
- Run `docker-compose run --rm django ./manage.py migrate`
- Run `docker-compose run --rm django ./manage.py createsuperuser` to create a super user to be able to create and manage the users from the django admin panel

## Tests
The project uses `pytest` framework for testing.

- Run tests `docker-compose run --rm django python -m pytest`