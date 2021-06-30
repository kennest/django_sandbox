!# /bin/bash
python manage.py runserver
celery -A django_sandbox worker -l INFO
celery flower --basic_auth=admin:flower -A django_sandbox
celery -A django_sandbox beat