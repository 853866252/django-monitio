import json

from django.core.mail import send_mail
from django_sse.redisqueue import send_event
from persistent_messages import constants


def email(level, message, extra_tags, subject, user, from_user):
    if not user or not user.email:
        raise Exception(
            'Function needs to be passed a `User` object with valid email address.')
    send_mail(subject, message, from_user.email if from_user else None,
              [user.email], fail_silently=False)


def sse(level, pk, message, extra_tags, subject, user, from_user):
    """
    :type user: basestring
    :type from_user: basestring
    """
    send_event("message",
               json.dumps(dict(
                   level=constants.DEFAULT_TAGS.get(level), pk=pk,
                   message=message,
                   extra_tags=extra_tags,
                   subject=subject, from_user=from_user)),
               channel=user)
