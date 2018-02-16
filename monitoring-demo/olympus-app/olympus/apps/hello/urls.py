from django.conf.urls import url

from .views import say_hello

urlpatterns = [
    url(r'^$', say_hello),
]
