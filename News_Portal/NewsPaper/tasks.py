from celery import shared_task
from django.contrib.auth.models import User
from .models import Post, Subscriber, PostCategory
from django.core.mail import EmailMultiAlternatives
import datetime

@shared_task
def send_if_post_created(instance_id, **kwargs):
    instance = Post.objects.get(pk=instance_id)
    postcategory_queryset = PostCategory.objects.filter(post=instance.pk)
    categories = [i.category for i in postcategory_queryset]
    subs_ids = set()
    for i in categories:
        for j in Subscriber.objects.filter(category=i).values_list('user'):
            subs_ids.add(j[0])
    subs_emails = set()
    for id in subs_ids:
        subs_emails.add(User.objects.get(pk=id).email)
    subject = f'Опубликован пост категории {instance.category}'
    text_content = (
        f'"{instance.title}"\n'
        f'Посмотреть пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'<h2>{instance.title}</h2><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in subs_emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
@shared_task
def send_news():
        last_exec_date= datetime.datetime.utcnow()-datetime.timedelta(weeks=1)
        print(f'{last_exec_date} / {datetime.datetime.utcnow()} / {datetime.timedelta(weeks=1)}' )
        '''new_posts = Post.objects.filter(date__gt=last_exec_date)
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
            print('не было новых постов')'''