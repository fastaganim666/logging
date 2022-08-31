from django.core.mail import mail_managers
from .models import Post, PostCategory, SubscribersCategory

from django.db.models import signals
from django.core.mail import send_mail
from django.contrib.auth.models import User


def notify_managers_appointment(sender, instance, **kwargs):
    mail_managers(
        subject='Пост удален',
        message="Пост удален",
    )
    print('пост удален')


signals.post_delete.connect(notify_managers_appointment, sender=Post)


def printer2(sender, instance, created, **kwargs):
    post_id = instance.post_id
    category_id = instance.category_id
    user_id = SubscribersCategory.objects.filter(category_id=category_id)
    user_id = list(user_id.values('user_id'))
    emails = []
    for user in user_id:
        email = User.objects.get(id=user['user_id']).email
        emails.append(email)
    print(emails)

    post = Post.objects.get(id=post_id)

    send_mail(
        subject=post.name,
        message=post.text,
        from_email='fastaganim666@yandex.ru',
        recipient_list=emails
    )
    print('PostCategory')


signals.post_save.connect(receiver=printer2, sender=PostCategory)
