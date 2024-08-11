from django import forms


class WineScoreForm(forms.Form):
    def __init__(self, wines, *args, **kwargs):
        super(WineScoreForm, self).__init__(*args, **kwargs)
        for i, wine in enumerate(wines):
            self.fields[f'wine_{wine.id}'] = forms.FloatField(
                min_value=0,
                max_value=10,
                widget=forms.NumberInput(attrs={
                    "placeholder": "Ta note",
                    "class": "form-control ms-2 me-2",
                })
            )

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Nom",
            "class": "form-control",
        })
    )

class UploadFileForm(forms.Form):
    files = forms.FileField(required=False)
    urls = forms.CharField(max_length=1000, required=False)

    def clean(self):
        cleaned_data = super().clean()
        files = cleaned_data.get("files")
        urls = cleaned_data.get("urls")

        if not files and not urls:
            raise forms.ValidationError("You must provide either a file or a list of URLs.")

        return cleaned_data