from django.conf.urls import patterns, url, include
from django.contrib import admin

from test_app.views import TestView

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TestView.as_view(), name='index'),
    url(r'^messages/', include('monitio.urls')),
)
