class LabelAdder(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs['placeholder'] = self.fields[key].label


class FormRequestMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
