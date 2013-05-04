from django.conf.urls.defaults import *

urlpatterns = patterns('persistent_messages.views',
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
)
