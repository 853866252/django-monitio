# This must be imported first - the DEFAULT_TAGS must be updated
# before import of monitio.api
import constants
import notify
from django.contrib import messages

messages.DEFAULT_TAGS.update(constants.DEFAULT_TAGS)

from monitio.api import *















