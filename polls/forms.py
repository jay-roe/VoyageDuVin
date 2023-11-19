from django import forms


# TODO this will need to be dynamic eventually
class NameForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
    vin1 = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
    vin2 = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
    vin3 = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
    vin4 = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
    vin5 = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
    vin6 = forms.FloatField(min_value=0, max_value=10, step_size=0.01)
