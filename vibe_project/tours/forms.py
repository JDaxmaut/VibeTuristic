from django import forms
from .models import TourPage, Departure


class BookingRequestForm(forms.Form):
    name = forms.CharField(
        label="Как тебя зовут?",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Имя", "required": True}),
    )
    contact = forms.CharField(
        label="Телефон или ник в Telegram",
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "+7 ··· / @username", "required": True}
        ),
    )
    tour = forms.ChoiceField(
        label="Какой тур интересует?",
        choices=[],
        required=False,
    )
    month = forms.ChoiceField(
        label="Удобный месяц",
        choices=[],
        required=False,
    )
    msg = forms.CharField(
        label="Комментарий или вопрос",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Например: едем вдвоём, остались ли места на 5-дневный тур в январе?",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tours = TourPage.objects.live()
        tour_choices = [("", "Выберите тур")]
        for t in tours:
            tour_choices.append((t.pk, t.title))
        self.fields["tour"].choices = tour_choices

        departures = Departure.objects.upcoming().order_by("date_from")
        month_choices = [("", "Выберите месяц")]
        seen = set()
        for d in departures:
            key = d.date_from.strftime("%Y-%m")
            if key not in seen:
                seen.add(key)
                label = d.date_from.strftime("%B %Y").capitalize()
                month_choices.append((key, label))
        self.fields["month"].choices = month_choices
