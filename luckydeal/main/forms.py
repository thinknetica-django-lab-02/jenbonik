from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.forms import CharField
from django.forms import DateField
from django.forms import DateInput
from django.forms import ModelForm
from django.forms import Textarea
from django.forms.models import inlineformset_factory

from main.models import UserProfile

import datetime


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


ALLOW_AGE_DAYS = (365 * 18) + (18 / 4)

class BirthDateField(DateField):
    def validate(self, value):
        super().validate(value)

        allow_date = value + datetime.timedelta(days = ALLOW_AGE_DAYS)

        delta = datetime.date.today() - value
        if datetime.date.today() < allow_date:
            raise ValidationError("Регистрация запрещена лицам младше 18 лет")    


UserProfileFormset = inlineformset_factory(User, 
    UserProfile, extra = 1, 
    fields = ('birth_date', 'description', 'image'),
    widgets = {
        'description': Textarea,
    })
