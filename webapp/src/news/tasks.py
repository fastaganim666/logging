from celery import shared_task
import time
from .models import Post, PostCategory, SubscribersCategory, Category
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.utils.timezone import now

import datetime
date = datetime.datetime.today()
week = date.strftime("%V")

year, week, _ = now().isocalendar()

@shared_task
def hello():
    time.sleep(2)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def weekly_mail():
    last_week = week
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