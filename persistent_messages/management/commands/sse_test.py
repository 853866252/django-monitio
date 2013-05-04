# -*- encoding: utf-8 -*-

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from persistent_messages import constants
from persistent_messages.notify import sse
from persistent_messages.views import SSE_ANONYMOUS


class Command(BaseCommand):
    help = '''This utility lets you send dynamic notifications (via Redis)
    to a logged-in OR anonymous user.

    Uwage: sse_test [user]'''

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(username=args[0]).username
        except (IndexError, User.DoesNotExist):
            user = SSE_ANONYMOUS

        print "Will send messages from ", user, "to", user
        while True:
            message = raw_input("message> ")
            sse(constants.INFO, -1, message, "", "Sent from manage.py command",
                user, user)
