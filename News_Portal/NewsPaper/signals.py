from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Subscriber, PostCategory
from django.core.mail import EmailMultiAlternatives

@receiver(m2m_changed, sender=Post.category.through)
def product_created(instance, **kwargs):
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
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in subs_emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()