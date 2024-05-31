from django import forms

class UploadForm(forms.Form):

    upload_file = forms.FileField(label='', help_text='', required=True)

    class Meta:
        fields = "upload_file"

    def clean_upload_file(self):
        file = self.cleaned_data.get('upload_file')
        if file:
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('O arquivo não pode ter mais de 5 MB.')
        return file