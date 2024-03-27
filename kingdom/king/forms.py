from django import forms
from .models import Kingdom

class ServantForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(min_value=18, max_value=100, label="Your Age")

    __data__ = Kingdom.objects.all()
    __choices__ = []
    for d in __data__:
        __choices__.append((d.id, d.name))

    kingdom = forms.ChoiceField(choices=__choices__, required=True, label="Kingdom", widget=forms.RadioSelect)

class TestForm(forms.Form):
    def __init__(self, question_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, q in enumerate(question_list, start=1):
            self.fields[f'question-{i}'] = forms.ChoiceField(
                choices=[(1,True), (0,False)],
                required=True, 
                widget=forms.RadioSelect(),
                label=q['question']
            )
