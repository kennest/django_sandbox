from django.shortcuts import render
from .tasks import download_large_file, my_task
# Create your views here.


def index(request):
    result = download_large_file.delay(10)
    return render(request, 'celery/index.html', context={'task_id': result.task_id})
