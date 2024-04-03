from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Kingdom

class ServantForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(min_value=18, max_value=100, label="Your Age")
    email = forms.EmailField(max_length=50, label="Your Email")

    __data__ = Kingdom.objects.all()
    __choices__ = []
    for d in __data__:
        __choices__.append((d.id, d.name))

    kingdom = forms.ChoiceField(choices=__choices__, required=True, label="Kingdom", widget=forms.RadioSelect)

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question_list = kwargs.pop('question_list')
        super().__init__(*args, **kwargs)
        for q in question_list:
            self.fields[f"question-{q['id']}"] = forms.ChoiceField(
                choices=[(1,True), (0,False)],
                required=True, 
                widget=forms.RadioSelect(),
                label=q['question']
            )

class SignInForm(forms.Form):
    email = forms.EmailField(max_length=50, label="Enter email")