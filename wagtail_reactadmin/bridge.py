import functools
import os
import pathlib

from django.contrib import messages
from django.middleware.csrf import get_token
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import conditional_escape
from rest_framework.response import Response as DRFResponse
from wagtail.admin.telepath import registry

from django_bridge.conf import DjangoBridgeConfig
from django_bridge.response import Response, process_response

from . import context_providers

VITE_DEVSERVER_URL = os.environ.get("VITE_DEVSERVER_URL")
config = DjangoBridgeConfig(
    bootstrap_template="wagtail_reactadmin/shell.html",
    framework="react",
    entry_point="src/main.tsx",
    vite_devserver_url=VITE_DEVSERVER_URL,
    vite_bundle_dir=pathlib.Path(__file__).parent / "static"
    if VITE_DEVSERVER_URL is None
    else None,
    context_providers={
        "csrf_token": get_token,
        "urls": context_providers.urls,
        "locales": context_providers.locales,
        "admin_api": context_providers.admin_api,
        "sidebar": context_providers.sidebar_props,
    },
    adapter_registry=registry,
)


def format_messages(messagelist):
    default_level_tag = messages.DEFAULT_TAGS[messages.SUCCESS]
    return [
        {
            "level": messages.DEFAULT_TAGS.get(message.level, default_level_tag),
            "html": conditional_escape(message.message),
        }
        for message in messagelist
    ]


def convert_response_to_django_bridge(view_func):
    """
    Converts legacy HTML responses to Django Bridge responses.

    This allows the response to be rendered without reloading the page.
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Extract existing messages, see message logic handling below
        previous_messages = list(messages.get_messages(request))

        # Run the view function
        response = view_func(request, *args, **kwargs)

        # Ignore Django REST framework responses
        if isinstance(response, DRFResponse):
            return response

        # TODO: Only wrap responses that have used the admin_base template
        if (
            response.status_code != 302
            and response["Content-Type"].startswith("text/html")
            and not request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        ):
            if isinstance(response, TemplateResponse):
                html = response.render().text
            else:
                html = response.content.decode("utf-8")

            response = Response(
                request,
                "HTMLPage",
                {
                    "html": html,
                    "frameUrl": reverse("shell-frame"),
                    "banners": [],
                },
            )

            # Wagtail uses messages to put static banners at the top of the page
            # If this request is a GET request, remove any new messages that were
            # inserted and put them in the "banners" prop so they are rendered at
            # the top of the page instead of as a toast message.
            if request.method == "GET":
                current_messages = list(messages.get_messages(request))
                response.props["banners"] = format_messages([
                    message for message in current_messages
                    if message not in previous_messages
                ])
                response.messages = format_messages(previous_messages)

        # Render the response with Django bridge
        # Note, the render_response helper acts like the django-bridge middleware
        return process_response(request, response, config)

    return wrapper
