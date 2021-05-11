from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from ckeditor.widgets import CKEditorWidget

from .models import Good as GoodModel
from .models import Category as CategoryModel
from .models import Tag as TagModel
from .models import Seller as SellerModel
from .models import Subscriber as SubscriberModel


@admin.register(GoodModel)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'seller')
    search_fields = ('category', 'seller', 'tags')
    ordering = (('name'), )
    fields = (('name', 'price'),
              ('description'),
              ('seller', 'category'),
              ('tags'))


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (('name'), )
    search_fields = (('name'), )
    ordering = (('name'), )


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = (('name'), )
    search_fields = (('name'), )
    ordering = (('name'), )


@admin.register(SellerModel)
class SellerAdmin(admin.ModelAdmin):
    list_display = (('name'), )
    search_fields = (('name'), )
    ordering = (('name'), )


@admin.register(SubscriberModel)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (('good'), )
    search_fields = (('good'), )
    ordering = (('good'), )


class FlatPageCK(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCK)
