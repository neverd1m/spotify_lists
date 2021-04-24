from django import forms
from models import Response_list


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response_list
