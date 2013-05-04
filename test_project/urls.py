from django.conf.urls import patterns, url, include
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_sse.redisqueue import RedisQueueView

from test_app.views import TestView
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TestView.as_view()),
    url(r'^messages/', include('persistent_messages.urls')),
)
