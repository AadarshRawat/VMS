# Vendor Management System

## Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/AadarshRawat/VMS
cd VMS
```

Create a virtual environment to install dependencies in and activate it:

```sh
python -m venv env
source env/bin/activate
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Once `pip` has finished downloading the dependencies:
```sh
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver
```

In order to test the  flows, documented postman collection is [attached](https://github.com/AadarshRawat/VMS/blob/main/VMS.postman_collection.json).

