from django.urls import path
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from wagtail.admin.urls import urlpatterns
from wagtail.utils.urlpatterns import decorate_urlpatterns

from .bridge import convert_response_to_django_bridge

urlpatterns = [
    path(
        "shell-frame/",
        xframe_options_sameorigin(
            TemplateView.as_view(template_name="wagtail_reactadmin/shellframe.html")
        ),
        name="shell-frame",
    ),
] + decorate_urlpatterns(urlpatterns, convert_response_to_django_bridge)
