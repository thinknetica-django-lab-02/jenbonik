from celery import shared_task
from django.core.mail import send_mail

from main.models import UserProfile
from main.models import Subscriber


@shared_task
def task_subscription():
    """ Отправка рассылок о новых товарах """
    subscriptions = Subscriber.objects.all()

    if subscriptions.count() == 0:
        return

    text_message = ''
    html_message = ''
    url = ''
    name = ''

    for subscribtion in subscriptions:
        url = subscribtion.good.get_absolute_url()
        name = subscribtion.good.name
        html_message += f'{html_message}<p><a href = "{url}">{name}</a></p>'
        text_message += f'{html_message}\n{name}'

    subscribers = UserProfile.objects.filter(is_subscriber=True)

    for subscriber in subscribers:
        send_mail("Новые поступления",
                  text_message,
                  None,
                  [subscriber.user.email],
                  html_message=html_message)

    for subscribtion in subscriptions:
        subscribtion.delete()
