from django import forms


class WriteForm(forms.Form):
    title = forms.CharField(label="title",max_length=1024)
    body = forms.CharField(label="body",widget=forms.Textarea)
