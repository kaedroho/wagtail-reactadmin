from django_bridge.adapters.registry import Adapter, register
from wagtail.admin.ui.sidebar import (
    ActionMenuItem,
    BaseSidebarAdapter,
    LinkMenuItem,
    MainMenuModule,
    PageExplorerMenuItem,
    SearchModule,
    SubMenuItem,
    WagtailBrandingModule,
)


def adapter(cls, js_constructor, base=Adapter):
    ClassAdapter = type(
        cls.__name__ + "Adapter",
        (base,),
        {
            "js_constructor": js_constructor,
            "js_args": lambda self, obj: obj.js_args(),
        },
    )

    register(ClassAdapter(), cls)


adapter(LinkMenuItem, "wagtail.sidebar.LinkMenuItem", base=BaseSidebarAdapter)
adapter(ActionMenuItem, "wagtail.sidebar.ActionMenuItem", base=BaseSidebarAdapter)
adapter(SubMenuItem, "wagtail.sidebar.SubMenuItem", base=BaseSidebarAdapter)
adapter(
    PageExplorerMenuItem,
    "wagtail.sidebar.PageExplorerMenuItem",
    base=BaseSidebarAdapter,
)
adapter(
    WagtailBrandingModule,
    "wagtail.sidebar.WagtailBrandingModule",
    base=BaseSidebarAdapter,
)
adapter(SearchModule, "wagtail.sidebar.SearchModule", base=BaseSidebarAdapter)
adapter(MainMenuModule, "wagtail.sidebar.MainMenuModule", base=BaseSidebarAdapter)
