from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.forms import CharField
from django.forms import DateField
from django.forms import DateInput
from django.forms import ModelForm
from django.forms import Textarea
from django.forms.models import inlineformset_factory

from main.models import UserProfile
from luckydeal.settings import ALLOW_AGE_DAYS

import datetime


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class BirthDateField(DateField):
    def validate(self, value):
        super().validate(value)

        allow_date = value + datetime.timedelta(days = ALLOW_AGE_DAYS)

        if datetime.date.today() < allow_date:
            raise ValidationError("Регистрация запрещена лицам младше 18 лет")    


UserProfileFormset = inlineformset_factory(User, 
    UserProfile, extra = 1, 
    fields = ('birth_date', 'description', 'is_subscriber', 'image'),
    field_classes = {
        'birth_date': BirthDateField, 
    },
    widgets = {
        'description': Textarea,
    })
