"""
Flask integration for the MDK.

This requires Flask and the blinker library.
"""

import atexit
import traceback

import mdk

from flask import (
    g, request, request_started, got_request_exception, request_tearing_down,
)

def _on_request_started(sender, **extra):
    """Create a new MDK session at request start."""
    g.mdk_session = sender.mdk.join(
        request.headers.get(sender.mdk.CONTEXT_HEADER))
    g.mdk_session.start_interaction()

def _on_request_exception(sender, **extra):
    """Fail interaction when a request handlers raises an error."""
    exc = extra.get("exception", None)
    g.mdk_session.fail_interaction(
        "".join(traceback.format_exception_only(exc.__class__, exc)))

def _on_request_tearing_down(sender, **extra):
    """Finish an interaction when a request is done."""
    g.mdk_session.finish_interaction()
    del g.mdk_session


def mdk_setup(app):
    """Setup MDK integration with Flask."""
    app.mdk = mdk.start()
    atexit.register(app.mdk.stop)
    request_started.connect(_on_request_started, app)
    got_request_exception.connect(_on_request_exception, app)
    request_tearing_down.connect(_on_request_tearing_down, app)


__all__ = ["mdk_setup"]
