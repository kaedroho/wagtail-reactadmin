# Wagtail ReactAdmin

A Wagtail plugin that turns the admin interface into a React SPA!

## Installation

First, install `wagtail_reactadmin` and `django_bridge`:

```sh
pip install wagtail_reactadmin django_bridge==0.6.0rc2
```

Then add `"wagtail_reactadmin"` to `INSTALLED_APPS` above `"wagtail.admin"`:

```python
INSTALLED_APPS = [
    ...
    "wagtail_reactadmin",
    "wagtail.admin",
    ...
]

Then, in your `urls.py`, replace the import for `wagtail.admin.urls` with `wagtail_reactadmin.urls`:

```python
from wagtail_reactadmin import urls as wagtailadmin_urls
...

urlpatterns = [
    ...
    path("admin/", include(wagtailadmin_urls)),
    ...
]
```

That's it!

## Project status

Currently this project is in alpha status, the left hand menu and toast messages aren't fully styled yet, and you may hit issues with certian Wagtail features (such as bulk actions).
