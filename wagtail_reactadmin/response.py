import json
import warnings

from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.utils.cache import patch_cache_control
from django.utils.html import conditional_escape

from django_bridge.conf import DjangoBridgeConfig
from django_bridge.metadata import Metadata
from django_bridge.response import BaseResponse, get_messages
from django_bridge.views import DjangoBridgeMixin as OriginalDjangoBridgeMixin


class Response(BaseResponse):
    """
    Instructs the client to render a view (React component) with the given context.
    """

    action = "render"

    def __init__(
        self,
        request,
        view,
        props,
        *,
        overlay=False,
        title="",
        metadata: Metadata | None = None,
        status=None,
        extra_entry_points=None,
    ):
        if metadata is None:
            if title:
                warnings.warn(
                    "The title argument is deprecated. Use metadata instead.",
                    PendingDeprecationWarning,
                )

            metadata = Metadata(title=title)
        elif title:
            raise TypeError("title and metadata cannot both be provided")

        super().__init__({}, status=status)
        self._request = request
        self.view = view
        self.props = props
        self.overlay = overlay
        self.metadata = metadata
        self.messages = get_messages(request)
        self.extra_entry_points = extra_entry_points or []

    def get_response_data(self, config):
        context = {
            name: provider(self._request)
            for name, provider in config.context_providers.items()
        }
        return config.pack(
            {
                "action": self.action,
                "view": self.view,
                "overlay": self.overlay,
                "metadata": self.metadata,
                "props": self.props,
                "context": context,
                "messages": self.messages,
            }
        )

    def as_htmlresponse(self, config):
        """
        Wrap response data in our bootstrap template to load the frontend bundle.
        """
        vite_react_refresh_runtime = None

        if config.vite_bundle_dir:
            # Production - Use asset manifest to find URLs to bundled JS/CSS
            asset_manifest = json.loads(
                (config.vite_bundle_dir / ".vite/manifest.json").read_text()
            )

            js = [
                static(asset_manifest[config.entry_point]["file"]),
            ]
            css = asset_manifest[config.entry_point].get("css", [])

            for entry_point in self.extra_entry_points:
                js.append(asset_manifest[entry_point]["file"])
                css.extend(asset_manifest[entry_point].get("css", []))

        elif config.vite_devserver_url:
            # Development - Fetch JS/CSS from Vite server
            js = [
                f"{config.vite_devserver_url}/@vite/client",
                f"{config.vite_devserver_url}/{config.entry_point}",
            ]

            for entry_point in self.extra_entry_points:
                js.append(f"{config.vite_devserver_url}/{entry_point}")

            css = []
            if config.framework == "react":
                vite_react_refresh_runtime = (
                    config.vite_devserver_url + "/@react-refresh"
                )

        else:
            raise ImproperlyConfigured(
                "DJANGO_BRIDGE['VITE_BUNDLE_DIR'] (production) or DJANGO_BRIDGE['VITE_DEVSERVER_URL'] (development) must be set"
            )

        response_data = self.get_response_data(config)
        response = render(
            self._request,
            config.bootstrap_template,
            {
                "metadata": response_data.get("metadata"),
                "initial_response": response_data,
                "js": js,
                "css": css,
                "vite_react_refresh_runtime": vite_react_refresh_runtime,
            },
        )

        response.status_code = self.status_code
        if self.cookies:
            response.cookies = self.cookies

        return response


class DjangoBridgeMixin(OriginalDjangoBridgeMixin):
    """A mixin that can be used to render a view with a React component."""

    response_class = Response
    extra_entry_points = []

    def render_to_response(self, props):
        """
        Return a response, using the `response_class` for this view, with a
        view rendered with the given props.

        Pass response_kwargs to the constructor of the response class.
        """
        return self.response_class(
            self.request,
            self.view_name,
            props,
            overlay=self.overlay,
            metadata=self.get_metadata(),
            extra_entry_points=self.extra_entry_points,
        )
