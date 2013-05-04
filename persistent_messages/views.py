from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_sse.redisqueue import RedisQueueView

from persistent_messages.models import Message
from persistent_messages.storage import get_user

SSE_ANONYMOUS = "__anonymous__"


def message_detail(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()

    return render_to_response('persistent_messages/message/detail.html',
                              {'message': message},
                              context_instance=RequestContext(request))


def message_delete(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    message = get_object_or_404(Message, user=user, pk=message_id)
    message.delete()

    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_delete_all(request):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    Message.objects.filter(user=user).delete()

    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_mark_read(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()

    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


def message_mark_all_read(request):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied

    Message.objects.filter(user=user).update(read=True)
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')


class DynamicChannelRedisQueueView(RedisQueueView):
    def get_redis_channel(self):
        return self.kwargs['channel'] or self.redis_channel


class SameUserChannelRedisQueueView(DynamicChannelRedisQueueView):
    redis_channel = SSE_ANONYMOUS

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print "X" * 90
        print request.user.is_anonymous()
        print self.get_redis_channel()

        pass_anon = request.user.is_anonymous() and self.get_redis_channel() == SSE_ANONYMOUS
        pass_logged_in = request.user.username == self.get_redis_channel()
        if pass_anon or pass_logged_in:
            return DynamicChannelRedisQueueView.dispatch(self, request, *args, **kwargs)
        return HttpResponseForbidden()

