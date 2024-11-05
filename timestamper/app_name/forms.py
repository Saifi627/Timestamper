from django import forms

class TimestampForm(forms.Form):
    timestamps = forms.CharField(widget=forms.Textarea, help_text="Enter timestamps in the format 'minutes:seconds - minutes:seconds'.")