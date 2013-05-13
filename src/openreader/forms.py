from django import forms

class NewFeedForm(forms.Form):
    url = forms.URLField(max_length=256, label="Enter the feed URL")