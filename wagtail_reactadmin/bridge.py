import functools
import os
import pathlib

from django.middleware.csrf import get_token
from django.template.response import TemplateResponse
from django.urls import reverse
from rest_framework.response import Response as DRFResponse

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
)


def convert_response_to_django_bridge(view_func):
    """
    Converts legacy HTML responses to Django Bridge responses.

    This allows the response to be rendered without reloading the page.
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
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
                {"html": html, "frameUrl": reverse("shell-frame")},
            )

        # Render the response with Django bridge
        # Note, the render_response helper acts like the django-bridge middleware
        return process_response(request, response, config)

    return wrapper
