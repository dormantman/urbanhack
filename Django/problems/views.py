import requests
from django import forms
from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from problems.models import Problem, Tag
from users.models import Profile


def index(request):
    return render(request, 'index.html')


def address_to_ll(address):
    geo_coder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geo_coder_params = {"geocode": address, "format": "json"}
    response = requests.get(geo_coder_api_server, params=geo_coder_params).json()

    try:
        object_raw = response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']
        coordinates = object_raw["Point"]["pos"]
        address = object_raw['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
        longitude, latitude = coordinates.split(' ')
    except KeyError:
        latitude, longitude = None, None

    return latitude, longitude, address


def ll_to_address(lat, long):
    lat = max(min(85.0, float(lat)), -85.0)
    long = max(min(179.0, float(long)), -179.0)

    geo_coder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geo_coder_params = {"geocode": f"{long},{lat}", "format": "json"}
    response = requests.get(geo_coder_api_server, params=geo_coder_params).json()

    try:
        object_raw = response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']
        coordinates = object_raw["Point"]["pos"]
        address = object_raw['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
        longitude, lattitude = coordinates.split()
    except KeyError:
        lattitude, longitude, address = lat, long, None

    return lattitude, longitude, address


class ProblemAddForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    # error_messages = {
    #     'password_mismatch': _("Пароли не совпадают."),
    # }

    title = forms.CharField(
        label=_("Заголовок"),
        widget=forms.TextInput,
        strip=True
    )
    description = forms.CharField(
        label=_("Описание"),
        widget=forms.TextInput,
        strip=True
    )
    photo = forms.FileField(
        label=_("Фото"),
        widget=forms.FileInput,
        required=False
    )
    tag = forms.ChoiceField(
        label=_("Тэг"),
        choices=[tuple([tag.name, tag.name]) for tag in Tag.objects.all()]
    )
    latitude = forms.FloatField(
        label=_("Широта")
    )
    longitude = forms.FloatField(
        label=_("Долгота")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        address = cleaned_data.get('address')

        try:
            if latitude and longitude:
                self.latitude, self.longitude, self.address = ll_to_address(latitude, longitude)
            elif address:
                self.latitude, self.longitude, self.address = address_to_ll(address)
            else:
                raise ValidationError('Отсутствует местоположение (координаты или адрес)')
        except Exception:
            raise ValidationError('Ошибка Yandex API')


class ProblemAdd(FormView):
    class Meta:
        model = Profile

    form_class = ProblemAddForm
    success_url = reverse_lazy('index')
    template_name = 'add.html'

    def form_valid(self, form):
        user = self.request.user
        problem = Problem(user=Profile.objects.get(user=user.pk), title=form['title'].data,
                          description=form['description'].data, photo=form['photo'].data,
                          tag=Tag.objects.get(name=form['tag'].data),
                          latitude=form.latitude, longitude=form.longitude, address=form.address)
        problem.save()

        return super().form_valid(form)


def problem_base(request):
    return render(request, 'list.html')
