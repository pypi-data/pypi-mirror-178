# Create app celery to start satellite_weather_downloader

from celery import Celery
from datetime import timedelta
from celery.signals import worker_ready

app = Celery("satellite_weather_downloader")

app.config_from_object("satellite_weather_downloader.celery_app.celeryconfig")


app.conf.beat_schedule = {
    # Executes every 0:01 a.m.
    'fetch-copernicus-weather-daily': {
        'task': 'fetch_copernicus_weather',
        'schedule': timedelta(hours=24),
    },
}


"""Send signal to run at worker startup"""


@worker_ready.connect
def at_start(sender, **kwargs):
    """Run tasks at startup"""
    with sender.app.connection() as conn:
        sender.app.send_task("fetch_copernicus_weather", connection=conn)
