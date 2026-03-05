from wagtail.admin.views.pages.edit import EditView
from wagtail_reactadmin.response import DjangoBridgeMixin


class ReactPageEditView(DjangoBridgeMixin, EditView):
    view_name = "page-edit"

    def get_context_data(self):
        # Django Bridge handles JSON serialisation so we can pass
        # the bound panel directly to the context
        bound_panel = self.edit_handler.get_bound_panel(
            instance=self.page, request=self.request, form=self.form
        )
        return {"edit_handler": bound_panel}
