from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse

from main.forms import UserForm
from main.forms import UserProfileFormset

from main.models import Good
from main.models import Tag
from main.models import UserProfile

def home(request):
    """ Возвращает главную страницу сайта """
    return render(request, 'main/index.html', 
        {
            'turn_on_block': True,
            'username': request.user.username, 
        })

@login_required(login_url = 'login')
def user_profile(request):
    """ Данные пользователя """
    user = request.user
    if request.method == 'POST':
        userform = UserForm(request.POST, request.FILES, instance = user)
        profileformset = UserProfileFormset(request.POST, request.FILES, instance = user)
        if profileformset.is_valid() and userform.is_valid():
            user.save()
            return HttpResponseRedirect(reverse('user_profile'))
    else:
        userform = UserForm(instance = user)
        profileformset = UserProfileFormset(instance = user)
    
    return render(request, 'main/userprofile_form.html', 
        {
            'userform': userform,
            'profileformset': profileformset
        })


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
