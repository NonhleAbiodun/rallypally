import random

from twilio.rest import Client

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ReceivedMessage


account_sid = settings.TWILIOSID
auth_token = settings.TWILIOTOKEN
client = Client(account_sid, auth_token)


def home(request):
    best_name = _get_best_name()
    email = _get_email(best_name)
    best_number = _get_best_number()
    best_zip = _get_best_zip()
    state = 'Oklahoma'
    return render(request, 'home.html', {
        'name': best_name,
        'email': email,
        'phone_number': best_number,
        'zip_code': best_zip,
        'state': state
    })


def messages(request):
    phone_number = request.GET['phone_number']
    messages = ReceivedMessage.objects.filter(
        twilio_number=phone_number
    )
    return render(request, 'messages.html', {
        'phone_number': phone_number,
        'messages': messages
    })

def _get_best_name():
    names = ['Dontre Hamilton', 'Eric Garner', 'John Crawford III',
             'Michael Brown Jr', 'Ezell Ford', 'Dante Parker',
             'Tanisha Anderson', 'Akai Gurley', 'Tamir Rice',
             'Rumain Brisbon', 'Jerame Reid', 'Tony Robinson',
             'Phillip White', 'Eric Harris', 'Walter Scott',
             'Freddie Gray', 'Trayvon Martin', 'Sandra Bland',
             'Breonna Taylor', 'George Floyd']
    return random.choice(names)


def _get_email(name):
    name = name.replace(' ', '')
    num = random.randrange(1, 999999)
    return '%s%s' % (name, num)


def _get_best_number():
    services = client.messaging.services.list(limit=20)
    # first go thru all available numbers and see if any are un-used
    unused_numbers = []
    for service in services:
        numbers = client.messaging.services(service.sid).phone_numbers.list(
            limit=100
        )
        for number in numbers:
            received_messages = ReceivedMessage.objects.filter(
                twilio_number=number.phone_number
            )
            if received_messages.count() == 0:
                unused_numbers.append(number.phone_number)
    if len(unused_numbers) > 0:
        return random.choice(unused_numbers)
    # if no un-used numbers are available, fall back to "least used" number
    return ReceivedMessage.objects.values('twilio_number').annotate(
        message_count=Count('id')
    ).order_by('-message_count')[0]['twilio_number']


def _get_best_zip():
    return '741%s%s' % (random.randrange(0,9), random.randrange(0,9))


@csrf_exempt
def sms_inbound(request):
    ReceivedMessage.objects.create(
        twilio_number=request.POST['To'],
        message=request.POST['Body'],
    )
    return HttpResponse(status=201)
