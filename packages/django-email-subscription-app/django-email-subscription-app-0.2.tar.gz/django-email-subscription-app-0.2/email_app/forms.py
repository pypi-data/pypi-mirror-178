from django import forms

class SubscribeForm(forms.Form):
    subscribe_check = forms.BooleanField(label="Subscribe", required=False)
    
