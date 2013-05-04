from django.conf.urls import patterns, url

from test_app.views import TestView

urlpatterns = patterns('',
    url(r'^$', TestView.as_view())
)
