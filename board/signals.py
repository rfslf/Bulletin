from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Bulletin, Reply

@receiver(post_save, sender=Reply)
def sending_reply(sender, instance, created, **kwargs):

    if created:
        pk = instance.bulletin_id
        pk_r = instance.id
        user_id = Bulletin.objects.get(pk=pk).author_id
        header = Bulletin.objects.get(pk=pk).header
        reply = Reply.objects.get(pk=pk_r)

        title = f'Новый отклик'
        msg = f'На объявление: {header} '\
            f'Содержание: {reply}'
        email = 'avdonin@unn.ru'
        user_email = User.objects.get(pk=user_id).email

#        send_mail(subject=title, message=msg, from_email=email, recipient_list=[user_email, ])
        print(title, msg, user_email)