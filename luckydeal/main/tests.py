from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from main.models import Category
from main.models import Country
from main.models import Good
from main.models import Seller
from main.models import Tag


class ViewTestCase(TestCase):
    """Базовый класс для проверки ответа представления"""
    def _testView(self, url_name, required_status=200, args=None):
        response = self.client.get(reverse(url_name, args=args))
        self.assertEqual(response.status_code, required_status)


class StaticPagesViewTestCase(ViewTestCase):
    """Проверка статических страниц сайта"""
    def testHomeView(self):
        self._testView('home')


class FlatPagesViewTestCase(ViewTestCase):
    """Проверка страниц сайта хранящихся в базе данных под управленем модуля flatpage"""
    @classmethod
    def setUpTestData(cls):
        sites = Site.objects.filter(pk=1)
        if(sites.count() == 0):
            cls.default_site = Site(pk=1, domain='example.com', name='example.com')
            cls.default_site.save()
        else:
            cls.default_site = sites[0]

    def _testFlatPageView(self, url, url_name, required_status=200, args=None):
        self.flatpage = FlatPage.objects.create(
            url=url, title='Тестовая страница', content="Тестовый контент",
            enable_comments=False, template_name='', registration_required=False)
        self.flatpage.sites.add(self.default_site)
        self._testView(url_name, required_status=required_status, args=args)   

    def testContactsView(self):
        self._testFlatPageView('/contacts/', 'contacts') 

    def testAboutView(self):
        self._testFlatPageView('/about/', 'about')


class GoodViewsTestCase(ViewTestCase):
    """Проверка страниц товаров"""
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(iso3 = 'RUS', name = 'Россия')
        seller = Seller.objects.create(name = 'МакроТехноПарк', country = country)
        tag = Tag.objects.create(name = 'для дома')
        category = Category.objects.create(name = 'Утюги')
        
        good = Good.objects.create(name = 'Bosh', description = 'Утюг Bosh', 
            category = category, seller = seller, price = 5000)
        good.tags.add(tag)

        cls.good_pk = good.pk

    def testGoodList(self):
        self._testView('goods')

    def testGoodAddView(self):
        self._testView('good_add', required_status=302)

    def testGoodDetailView(self):
        self._testView('good_detail', args=[self.good_pk])

    def testGoodUpdateView(self):
        self._testView('good_edit', required_status=302, args=[self.good_pk])


class AuthViewsTestCase(ViewTestCase):
    """Проверка страниц аутентификации"""
    
    def testUserLogin(self):
        self._testView('login')

    def testUserProfile(self):
        self._testView('user_profile', required_status=302)
