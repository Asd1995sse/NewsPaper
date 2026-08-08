from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Добавляем задачу: еженедельная рассылка
    scheduler.add_job(
        call_command,
        args=['send_weekly_newsletter'],
        trigger=IntervalTrigger(weeks=1),
        id='weekly_newsletter',
        replace_existing=True,
    )
    scheduler.start()
    logger.info("OK! Планировщик еженедельной рассылки запущен")