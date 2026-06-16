from django import forms

from .models import DIFFICULTY_CHOICES, TOPIC_CHOICES


class StartTestForm(forms.Form):
    MODE_CHOICES = [
        ("standard", "Стандартный тест"),
        ("agent", "ИИ-агент"),
    ]

    full_name = forms.CharField(
        label="ФИО",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Иванов Иван Иванович"}),
    )

    group_name = forms.CharField(
        label="Группа",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Например: ИСП-21"}),
    )

    topic = forms.ChoiceField(
        label="Тема",
        choices=TOPIC_CHOICES,
    )

    difficulty = forms.ChoiceField(
        label="Сложность",
        choices=DIFFICULTY_CHOICES,
        help_text="В режиме ИИ-агента сложность будет подобрана автоматически.",
    )

    mode = forms.ChoiceField(
        label="Режим",
        choices=MODE_CHOICES,
        initial="standard",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "mode":
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control form-control-lg"})

        self.fields["topic"].widget.attrs.update({"class": "form-select form-select-lg"})
        self.fields["difficulty"].widget.attrs.update({"class": "form-select form-select-lg"})
