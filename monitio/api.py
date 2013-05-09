from django.core.handlers.wsgi import WSGIRequest
from monitio import notify
from monitio import constants

def add_message(request, level, message, extra_tags='', fail_silently=False,
                subject='', user=None, email=False, sse=True, from_user=None,
                expires=None, close_timeout=None):
    """
    """
    if email:
        # TODO: django-post-trans sign dispatch() at the end of transsaction
        notify.email(level, message, extra_tags, subject, user, from_user)

    if sse:
        # TODO: django-post-trans signal dispatch() at the end of transaction
        raise NotImplementedError

    return request._messages.add(level, message, extra_tags, subject, user,
                                 from_user, expires, close_timeout)


def info(request, message, extra_tags='', fail_silently=False, subject='',
         user=None, email=False, from_user=None, expires=None,
         close_timeout=None):
    """
    """
    level = constants.INFO
    return add_message(request, level, message, extra_tags, fail_silently,
                       subject, user, email, from_user, expires, close_timeout)


def warning(request, message, extra_tags='', fail_silently=False, subject='',
            user=None, email=False, from_user=None, expires=None,
            close_timeout=None):
    """
    """
    level = constants.WARNING
    return add_message(request, level, message, extra_tags, fail_silently,
                       subject, user, email, from_user, expires, close_timeout)


def debug(request, message, extra_tags='', fail_silently=False, subject='',
          user=None, email=False, from_user=None, expires=None,
          close_timeout=None):
    """
    """
    level = constants.DEBUG
    return add_message(request, level, message, extra_tags, fail_silently,
                       subject, user, email, from_user, expires, close_timeout)


def create_message(to_user, from_user, level, message, extra_tags='',
                   subject='', expires=None, close_timeout=None, sse=True):
    """
    Use this method to create message without a request object - this can
    be used in command-line utilities or for testing.
    """

    from monitio.storage import PersistentMessageStorage
    class request:
        user = to_user
        session = {}

    request.messages = PersistentMessageStorage(request)

    request.messages.add(level=level, message=message, extra_tags=extra_tags,
                         subject=subject, from_user=from_user, expires=expires,
                         close_timeout=close_timeout, sse=sse)