from django.db import models

import uuid


class BaseIdentificatedObject(models.Model):
    id = models.UUIDField(auto_created = True, primary_key = True, 
        verbose_name = 'Идентификатор', default = uuid.uuid4, editable = False)
    
    class Meta:
        abstract = True


class Good(BaseIdentificatedObject):
    name = models.CharField(max_length = 200, verbose_name = 'Наименование', 
        help_text = 'Наименование', default = '')
    description = models.CharField(max_length = 500, verbose_name = 'Описание', 
        help_text = 'Подробное описание', default = '')
    price = models.DecimalField(max_digits = 10, decimal_places = 2, 
        verbose_name = 'Цена', help_text = 'Цена товара')
    category = models.ForeignKey('Category', on_delete = models.PROTECT,
        verbose_name = 'Категория', help_text = 'Категория товара',
        related_name = 'goods')
    seller = models.ForeignKey('Seller', on_delete = models.PROTECT,
        verbose_name = 'Продавец', help_text = 'Продавец товара',
        related_name = 'goods')
    tags = models.ManyToManyField('Tag', related_name = 'goods',
        verbose_name = 'Тэги', help_text = 'Тэги')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(BaseIdentificatedObject):
    name = models.CharField(max_length = 50, verbose_name = 'Наименование', 
        help_text = 'Наименование', default = '')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(BaseIdentificatedObject):
    name = models.CharField(max_length = 30, verbose_name = 'Наименование', 
        help_text = 'Наименование', default = '')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Seller(BaseIdentificatedObject):
    name = models.CharField(max_length = 50, verbose_name = 'Наименование', 
        help_text = 'Наименование', default = '')
    country = models.ForeignKey('Country', on_delete = models.PROTECT,
        verbose_name = 'Страна', help_text = 'Страна',
        related_name = 'sellers')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавец'


class Country(BaseIdentificatedObject):
    iso3 = models.CharField(max_length = 3, verbose_name = 'ISO3', 
        help_text = 'ISO3', default = '')
    name = models.CharField(max_length = 50, verbose_name = 'Наименование', 
        help_text = 'Наименование', default = '')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
