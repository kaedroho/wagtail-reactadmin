# Wagtail ReactAdmin

A Wagtail plugin that turns the admin interface into a React SPA!

Goals:

- Make Wagtail feel like a modern web app, with fast page loads, animations, and modern UI features
- Add new interfaces to Wagtail with pure React
- Full backwards compatibility for all HTML rendered views

Current status:

 - It works!
 - Some styling left to do on the sidebar and the toast messages
 - Bulk actions are broken
 - Some forms submissions (such as locking/unlocking pages) are not yet ajaxified
 - UI framework for building new interfaces being worked on

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
```

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

That's it! Your admin is now a React app
