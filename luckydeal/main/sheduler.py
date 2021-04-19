from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from luckydeal.settings import SECONDS_IN_WEEK

from main.models import UserProfile
from main.models import Subscriber

def send_subscribtions():
    subscriptions = Subscriber.objects.all()

    if subscriptions.count() == 0:
        return

    text_message = ''
    html_message = ''

    for subscribtion in subscriptions:
        html_message = f'{html_message}<p><a href = "{subscribtion.good.get_absolute_url()}">{subscribtion.good.name}</a></p>'
        text_message = f'{html_message}\n{subscribtion.good.name}'
    
    subscribers = UserProfile.objects.filter(is_subscriber = True)

    for subscriber in subscribers:
        send_mail("Новые поступления", text_message, None, [subscriber.user.email], 
                html_message = html_message)
    
    for subscribtion in subscriptions:
        subscribtion.delete()   


def sheduler_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_subscribtions, 'interval', seconds = 20)
    scheduler.start()