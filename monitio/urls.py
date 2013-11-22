from django.conf.urls import patterns, url
from monitio.views import SameUserChannelRedisQueueView

urlpatterns = patterns(
    'monitio.views',
    url(r'^detail/(?P<message_id>\d+)/$', 'message_detail',
        name='message_detail'),

    # Mark read
    url(r'^mark_read/(?P<message_id>\d+)/$', 'message_mark_read',
        name='message_mark_read'),
    url(r'^mark_read/all/$', 'message_mark_all_read',
        name='message_mark_all_read'),

    # Delete
    url(r'^delete/message/(?P<message_id>\d+)/$', 'message_delete',
        name='message_delete'),
    url(r'^delete/all/$', 'message_delete_all', name='message_delete_all'),

    # django-sse
    url(r'^sse/(?P<channel>\w+)?$',
        SameUserChannelRedisQueueView.as_view(), name="persistent-messages-sse"),


)
