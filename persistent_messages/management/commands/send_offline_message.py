import sys

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from persistent_messages import api


def err(msg, status=-1):
    sys.stderr.write('%s: %s\n' % (sys.argv[0], msg))
    sys.exit(status)


def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        err("No such user: %r" % username)

class Command(BaseCommand):
    args = 'from_user to_user message'
    help = '''Send an offline message

    Usage: send_offline_message [from user] [to user] [message]'''

    def handle(self, *args, **options):
        try:
            from_user, to_user = [get_user(username) for username in args[:2]]
        except ValueError:
            err(self.help)

        message = " ".join(args[2:])
        api.add_message_without_storage(level=api.constants.INFO,
        	from_user=from_user, to_user=to_user, message=message)
