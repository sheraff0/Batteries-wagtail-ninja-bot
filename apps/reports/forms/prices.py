from django import forms

from contrib.utils.excel.pandas import XlsxReader


class PriceListForm(forms.Form):
    action = forms.CharField()
    upload = forms.FileField(required=False)

    def clean_upload(self):
        try:
            file = self.cleaned_data["upload"]
            return XlsxReader(file).output
        except: ...
