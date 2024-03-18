from django import forms

from .models import Birthday


class BirthdayForm(forms.ModelForm):
    """Форма ввода дня рождения на основе модели."""
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'
        # Для поля с датой рождения используется виджет с типом данных date
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
