from django.conf.urls import patterns, url, include
from django.contrib import admin

from test_app.views import TestView
from views import TestFoundationView

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TestView.as_view(), name='index'),
    url(r'^foundation/$', TestFoundationView.as_view(), name='foundation'),
    url(r'^messages/', include('monitio.urls', namespace="monitio"))
)
