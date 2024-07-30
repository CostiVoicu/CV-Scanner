# CV-Scanner

- [Steps for Setting Up the Project Locally](#steps-for-setting-up-the-project-locally)
    - [Create virtual environment](#create-virtual-environment)
    - [Activate virtual environment](#activate-virtual-environment)
    - [Install the required packages](#install-the-required-packages)
    - [Add environment variables](#add-environment-variables)
    - [Apply the migrations](#apply-the-migrations)
    - [Run Django project](#run-django-project)
- [Steps for Setting Up the Project Using Docker](#steps-for-setting-up-the-project-using-docker)
    - [Build the docker images and run the containers](#build-the-docker-images-and-run-the-containers)

## Steps for setting up the project locally

### Create virtual environment
```bash
python -m venv .venv
```

### Activate virtual environment
```bash
source .venv/Scripts/activate
```

### Install the required packages
```bash
pip install -r requirements.txt
```

### Add environment variables
In the root directory, create a file called *.env*.
Declare your environment variables in *.env*. Use them to make a connection with an already existing PostgreSQL database.
```
SECRET_KEY=
DEBUG=
ALLOWED_HOST=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```

### Apply the migrations
```bash
py manage.py migrate
```

### Run Django project
```bash
py manage.py runserver
```

## Steps for setting up the project using docker

### Build the docker images and run the containers
```bash
docker-compose up --build
```