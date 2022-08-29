from django.core.mail import mail_managers
from .models import Post, PostCategory

from django.db.models import signals
from django.core.mail import send_mail




def notify_managers_appointment(sender, instance, **kwargs):
    mail_managers(
        subject='Пост удален',
        message="Пост удален",
    )
    print('пост удален')
signals.post_delete.connect(notify_managers_appointment, sender=Post)



def printer(sender, instance, created, **kwargs):
    send_mail(
        subject=instance.name,
        message=instance.text,
        from_email='fastaganim666@yandex.ru',
        recipient_list=['fastaganim666@gmail.com']
    )
    post_id = instance.id


signals.post_save.connect(receiver=printer, sender=Post)

def printer2(sender, instance, created, **kwargs):
    send_mail(
        subject=instance.post_id,
        message=instance.category_id,
        from_email='fastaganim666@yandex.ru',
        recipient_list=['fastaganim666@gmail.com']
    )
    print('PostCategory')


signals.post_save.connect(receiver=printer2, sender=PostCategory)
