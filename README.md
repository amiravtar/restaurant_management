# Restaurant Management System
A management system for online restaurants written in **Django**


## How to run

#### Optional: Creating python virtual environment

```shell
python -m venv env
source env/bin/activate 
```

### Install requirments

```shell
pip install -r requirements.txt
```
### Run migrations & Creat super user
```shell
python manage.py migrate
python manage.py createsuperuser
```

### optional: Load some default data with fixtures
```shell
python scripts/load_data.py
```

### Run django server

```shell
python manage.py runserver
```

and open http://localhost/admin in browser
