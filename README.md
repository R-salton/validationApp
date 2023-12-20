### Setting Up The Project
## 1: Installing Requirements
Run: ```pip install requirements.txt``` to install requirements
## 2: Setting .env File for Credentials
## 1. Crate .env file in The root directory and Add the following value
```DJANGO_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxx'```
replace xxxxxxxxxxxxxxx with the value of your SECRET_KEY
##  3: Setting dotenv in settings.py

```
import os
from dotenv import load_dotenv
load_dotenv()
----
SECRET_KEY = os.environ.get('DJANGO_SECRET')
```
## 4: Run Migrations
1. ```python manage.py makemigrations``` on Windows and ```python3 manage.py makemigartions``` for linux
2. ```python manage.py migrate``` on Windows and ```python3 manage.py migrate``` for linux
## 5: Run The App
```python manage.py runserver``` on Windows and ```python3 manage.py runserver``` for linux
