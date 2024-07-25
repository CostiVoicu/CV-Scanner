# CV-Scanner

- [Steps for building the project](#steps-for-building-the-project)
    - [Create virtual environment](#create-virtual-environment)
    - [Activate virtual environment](#activate-virtual-environment)
    - [Install the required packages](#install-the-required-packages)
- [Add environment variables](#add-environment-variables)
- [Apply the migrations](#apply-the-migrations)
- [Run Django project](#run-django-project)

## Steps for building the project

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

## Add environment variables
In the same directory as *settings.py*, create a file called *.env*.
Declare your environment variables in *.env*.
```
SECRET_KEY=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```

## Apply the migrations
```bash
py manage.py migrate
```

## Run Django project
```bash
py manage.py runserver
```
