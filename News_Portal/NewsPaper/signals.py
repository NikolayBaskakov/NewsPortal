from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Subscriber, PostCategory
from django.core.mail import EmailMultiAlternatives
from .tasks import send_if_post_created
@receiver(m2m_changed, sender=Post.category.through)
def post_created(sender, instance, action, **kwargs):
    if action == 'post_add' and instance.__class__.__name__ == 'Post':
        send_if_post_created.delay(instance_id=instance.id)