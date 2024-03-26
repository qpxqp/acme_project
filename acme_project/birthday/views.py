from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
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


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayListView(BirthdayMixin, ListView):
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin,
                         LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin,
                         OnlyAuthorMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, OnlyAuthorMixin, DeleteView):
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


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')
