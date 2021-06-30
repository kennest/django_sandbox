from django_sandbox.settings import MEDIA_ROOT
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import requests
import time
import os


@shared_task(bind=True)
def download_large_file(self, seconds):
    downloaded = 0
    progress_recorder = ProgressRecorder(self)
    url = "http://ipv4.download.thinkbroadband.com:8080/50MB.zip"
    response = requests.get(url, stream=True)
    file_size = response.headers['Content-length']
    file_name = url.split("/")[-1]
    file_name = os.path.join(MEDIA_ROOT, file_name)
    #print(f"File Path => {file_name}")
    with open(file_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                downloaded = downloaded+len(chunk)
                progress_recorder.set_progress(
                    downloaded, int(file_size))
        return downloaded


@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(seconds):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result
