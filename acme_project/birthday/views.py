from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday


class BirthdayFormMixin:
    form_class = BirthdayForm


class BirthdayListView(BirthdayMixin, ListView):
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(BirthdayMixin, DetailView):

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
