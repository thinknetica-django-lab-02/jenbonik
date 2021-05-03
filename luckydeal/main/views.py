from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from main.forms import UserForm
from main.forms import UserProfileFormset

from main.models import Good
from main.models import Tag
from main.models import UserProfile


@method_decorator(cache_page(settings.CACHE_TTL), name='dispatch')
class HomeView(TemplateView):
    """ Возвращает главную страницу сайта """   
    
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turn_on_block'] = True
        context['username'] = self.request.user.username
        return context


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    """ Редактирование профиля пользователя """
    
    model = User
    template_name = 'main/userprofile_form.html'
    success_url = '/accounts/profile/'
    form_class = UserForm

    def get_object(self, request):
        return request.user

    def get_context_data(self, **kwargs):
        profileformset = UserProfileFormset(instance = self.get_object(kwargs['request']))
        context = super().get_context_data(**kwargs)
        context['profileformset'] = profileformset
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object(request)
        profileformset = UserProfileFormset(self.request.POST, self.request.FILES, instance = self.object)
        
        if profileformset.is_valid() and form.is_valid():
            self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())

class GoodListView(ListView):
    """ Представление списка товаров """
    
    model = Good
    context_object_name = 'object_list'
    template_name = 'main/good_list.html'
    paginate_by = 10

    def get_queryset(self):
        tag_list = self.request.GET.getlist('tag', [])
        if tag_list == []:
            return Good.objects.order_by('name')
        else:
            return Good.objects.filter(tags__in = tag_list).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(goods__in = Good.objects.all()).distinct()
        tag_filter = self.request.GET.getlist('tag', [])
        tag_filter_str = ""
        for tag_id in tag_filter:
            tag_filter_str = tag_filter_str + tag_id + ","
        context['tag_filter_str'] = tag_filter_str[:-1]
        context['tag_filter'] = Tag.objects.filter(id__in = tag_filter).order_by('name')
        return context


@method_decorator(cache_page(settings.CACHE_TTL), name='dispatch')
class GoodDetailView(DetailView):
    """ Представление товара """
    
    model = Good
    template_name = 'main/good_detail.html'


class GoodCreate(PermissionRequiredMixin, CreateView):
    """ Создание товара """
    
    model = Good
    permission_required = 'main.add_Good'
    template_name = 'main/good_create.html'
    fields = ('name', 'description', 'price', 'category', 'seller', 'tags', 'image', )


class GoodUpdate(PermissionRequiredMixin, UpdateView):
    """ Создание товара """
    
    model = Good
    permission_required = 'main.change_Good'
    template_name = 'main/good_edit.html'
    fields = ('name', 'description', 'price', 'category', 'seller', 'tags', 'image', )
