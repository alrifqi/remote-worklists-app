from __future__ import absolute_import, unicode_literals

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from Fetcher.models import Company
from Fetcher.views import fetch_works

logger = get_task_logger(__name__)

@periodic_task(
    run_every=crontab(),
    name="task_print",
    ignore_result=True
)
def task_print():
    logger.info('start task print')
    fetch_works()
    logger.info('end task print')