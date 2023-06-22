# drf-base
Basic Django-Rest-Framework Application including:
* models
* custom migration
* serializers
* function based views
* class based views
* concrete views
* pagination
* permissions
* authentication

```
python -m venv env
```
```
source env/bin/activate
```
```
pip install -r requirements.txt
```
```
cd newsproject/
```
```
python manage.py migrate
```
```
python manage.py runserver
```

And go to:

http://127.0.0.1:8000/api/articles
