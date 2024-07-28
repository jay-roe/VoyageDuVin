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
    file = forms.FileField()