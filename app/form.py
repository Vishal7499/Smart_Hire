from django import forms

class feedback_form(forms.Form):
    my_choices = (
        ('10' , '10'),
        ('9' , '9'),
        ('8' , '8'),
        ('7' , '7'),
        ('6' , '6'),
        ('5' , '5'),
        ('4' , '4'),
        ('3' , '3'),
        ('2' , '2'),
        ('1' , '1'),
    )

    q1 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q2 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q3 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q4 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q5 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q6 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q7 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q8 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q9 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q10 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q11 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q12 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q13 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q14 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    q15 = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices = my_choices, required=True)
    