from django.db.models.fields.files import FileField
from django.utils.translation import ugettext_lazy as _
from django import forms


class ContentTypeRestrictedFileField(FileField):
    """
    FileField that handles the content_type and max_file_size of file field.

    2.5MB - 2621440
    5MB - 5242880
    10MB - 10485760
    20MB - 20971520
    50MB - 5242880
    100MB 104857600
    250MB - 214958080
    500MB - 429916160

    required: content_types
              max_upload_size

    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_file_upload_size = kwargs.pop('max_upload_size', None)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)
        # post update help_text
        # self.help_text += "`allowed types`: {}, `max_file_size`: {} MB"\
        #     .format(', '.join(self.content_types), str(self.max_file_upload_size))

    def clean(self, value, model_instance):
        # clean the field
        data = super(ContentTypeRestrictedFileField, self).clean(value=value, model_instance=model_instance)

        uploaded_file = data.file
        try:
            if (uploaded_file.content_type in self.content_types) or (self.content_types == "__all__"):
                if uploaded_file._size > self.max_file_upload_size:
                    raise forms.ValidationError(_("The allowed file size is {}. Current filesize: {}".
                                                  format(self.max_file_upload_size, uploaded_file._size)))
            else:
                raise forms.ValidationError(_("Filetype not supported."))
        except AttributeError:
            pass
        return data
