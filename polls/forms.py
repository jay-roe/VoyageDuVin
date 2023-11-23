from django import forms


class WineScoreForm(forms.Form):
    def __init__(self, wines, *args, **kwargs):
        super(WineScoreForm, self).__init__(*args, **kwargs)
        for i, wine in enumerate(wines):
            self.fields[f'wine{i+1}'] = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
            self.fields[f'wine{i+1}'].widget.attrs.update({
                "placeholder": "Ta note",
                "class": "form-control w-50 ms-2 me-2",
            })

    name = forms.CharField(max_length=100)
    name.widget.attrs.update({
        "placeholder": "Nom",
        "class": "form-control w-50",
    })
