from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.test import Client
from django.urls import reverse

from main.models import Category
from main.models import Country
from main.models import Good
from main.models import Seller
from main.models import Tag

import pytest


client = Client()

def response_status_code_assertion(url_name:str, required_status: int):
    response = client.get(reverse(url_name))
    assert(response.status_code == required_status)    


@pytest.mark.django_db
@pytest.mark.parametrize('url_name',
                         ['home'])
def test_static_pages(url_name):
    """Проверка статических страниц сайта"""
    response_status_code_assertion(url_name, 200)


@pytest.mark.django_db
@pytest.mark.parametrize('url, url_name',
                         [('/about/', 'about'), 
                         ('/contacts/', 'contacts')])
def test_flatpages(url, url_name):
    """Проверка сохраняемых в базу страниц сайта"""
    sites = Site.objects.filter(pk=1)
    if(sites.count() == 0):
        default_site = Site(pk=1, domain='example.com', name='example.com')
        default_site.save()
    else:
        default_site = sites[0]

    flatpage = FlatPage.objects.create(
        url=url, title='Тестовая страница', content="Тестовый контент",
        enable_comments=False, template_name='', registration_required=False)
    flatpage.sites.add(default_site)

    response_status_code_assertion(url_name, 200)


@pytest.mark.django_db
@pytest.mark.parametrize('url_name, required_status, use_good_id',
                         [('goods', 200, False),
                          ('good_add', 302, False),
                          ('good_detail', 200, True),
                          ('good_edit', 302, True)])
def test_good_pages(url_name, required_status, use_good_id):
    """Проверка страниц товаров"""

    if use_good_id == True:
        country = Country.objects.create(iso3 = 'RUS', name = 'Россия')
        seller = Seller.objects.create(name = 'МакроТехноПарк', country = country)
        tag = Tag.objects.create(name = 'для дома')
        category = Category.objects.create(name = 'Утюги')
            
        good = Good.objects.create(name = 'Bosh', description = 'Утюг Bosh', 
            category = category, seller = seller, price = 5000)
        good.tags.add(tag)

        url = reverse(url_name, args=[good.id])
    else:
        url = reverse(url_name)

    response = client.get(url)
    assert(response.status_code == required_status)



@pytest.mark.django_db
@pytest.mark.parametrize('url_name, required_status',
                         [('login', 200),
                          ('user_profile', 302)])
def test_auth_pages(url_name, required_status):
    """Проверка страниц аутентификации"""
    response_status_code_assertion(url_name, required_status)
