from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management import call_command
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
logger = get_task_logger(__name__)


@task(name="get_blocks")
def get_blocks():
    """
    This method removes all blacklisted tokens.
    Version: 1.0
    """
    import datetime
    from helpers.fetcher import fetch_blocs
    # local import of model, otherwise it won't work
    fetch_blocs(date=(datetime.date.today() - datetime.timedelta(days=1)).isoformat())
