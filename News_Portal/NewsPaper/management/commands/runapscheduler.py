import logging
from django.core.mail import send_mail
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives

from NewsPaper.models import Post, PostCategory, Subscriber

logger = logging.getLogger(__name__)


def my_job():
    try:
        last_exec_date= DjangoJobExecution.objects.filter(job_id='my_job').order_by('-id')[0].run_time
        new_posts = Post.objects.filter(date__gt=last_exec_date)
        if new_posts:
            for u in User.objects.all():
                sub_categories = Subscriber.objects.filter(user=u).values_list('category')
                message = f''
                html = f''
                for p in new_posts:
                    post_categories_ids = PostCategory.objects.filter(post=p).values_list('category')
                    flag = False
                    for c in post_categories_ids:
                        if c in sub_categories:
                            flag = True
                            break
                    if flag:
                        message += f'http://127.0.0.1:8000/{p.pk} \n'
                        html += f'<a href="http://127.0.0.1:8000/{p.pk}">Пост №{p.pk}</a><br>'
                if message:
                    message = f'Новые посты по вашим категориям: \n' + message
                    html = f'<h2>Новые посты по вашим категориям: </h2><br>' + html
                    msg = EmailMultiAlternatives('Новые посты по вашим категориям', message, None, [u.email])
                    msg.attach_alternative(html, "text/html")
                    msg.send()
                else:
                    print(f'для пользователя {u.email} нет постов по подпискам')
        else:
            print('не было новых постов')
    except IndexError: #исключение, если база выполненных работ пуста
        pass


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour='18', minute='00'),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")