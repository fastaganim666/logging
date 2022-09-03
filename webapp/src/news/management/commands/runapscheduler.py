# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.utils.timezone import now
from django.contrib.auth.models import User

from django.core.mail import send_mail

import datetime
date = datetime.datetime.today()
week = date.strftime("%V")

from ...models import Post, PostCategory, SubscribersCategory, Category

logger = logging.getLogger(__name__)

date = datetime.datetime.today()
week = date.strftime("%V")
year, week, _ = now().isocalendar()



def my_job():
    last_week = week - 1
    posts = Post.objects.filter(time_add__week=last_week)
    cats = [] # {1, 5}
    posts_list = [] # [107, 108, 109, 110, 111]
    for post in posts:
        posts_list.append(post.id)

    for post_id in posts_list:
        cat = PostCategory.objects.filter(post_id=post_id)
        cat = list(cat.values('category_id'))
        for c in cat:
            cats.append(c['category_id'])
    cats = set(cats)

    dict_cats = {} # {1: [108, 109, 110, 111], 5: [107, 111]}

    for key in cats:
        for post_id in posts_list:
            if PostCategory.objects.filter(post_id=post_id, category_id=key).exists():
                dict_cats[key] = dict_cats.get(key, []) + [post_id]

    all_users = SubscribersCategory.objects.all()

    users = {} # {1: ['', 'fastaganim666@gmail.com'], 3: ['', 'fastaganim666gmail.com@mail.ru'],
    # 5: ['fastaganim666@gmail.com', 'fastaganim666gmail.com@mail.ru', 'fastaganim666@gmail.com'],
    # 4: ['fastaganim666gmail.com@mail.ru']}

    for user in all_users:
        users[user.category_id] = users.get(user.category_id, []) + [User.objects.get(id=user.user_id).email]


    for cat in dict_cats:
        message = Category.objects.get(id=cat).name + ': '
        print(dict_cats[cat])
        for post_id in dict_cats[cat]:
            message += Post.objects.get(id=post_id).name + ' / '
        users[cat] = list(set(users[cat]))
        send_mail(
            subject=Category.objects.get(id=cat).name,
            message=message,
            from_email='fastaganim666@yandex.ru',
            recipient_list=users[cat]
        )




# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")