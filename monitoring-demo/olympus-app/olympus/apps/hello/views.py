from statsd.defaults.django import statsd

from django.http import HttpResponse


def say_hello(request):
    statsd.incr('hello.requests.total')
    return HttpResponse('Hello, World!')
