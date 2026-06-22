from django import forms


class StartTestForm(forms.Form):
    full_name = forms.CharField(
        label="ФИО",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Иванов Иван Иванович",
            }
        ),
    )

    group_name = forms.CharField(
        label="Группа",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Например: ИСП-21",
            }
        ),
    )
