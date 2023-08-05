# -*- coding: utf-8 -*-
"""  peony-twitter

    An asynchronous Twitter API client for Python
"""

__author__ = "Florian Badie"
__author_email__ = "florianbadie@gmail.com"
__url__ = "https://github.com/odrling/peony-twitter"

__version__ = "0.3"

__license__ = "MIT License"

__keywords__ = "twitter, asyncio, asynchronous"

from .client import PeonyClient, BasePeonyClient
from .commands import EventStream, task, event_handler, events
from .utils import handler_decorator
