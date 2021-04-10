from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

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


class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['email', 'first_name', 'last_name']
    template_name = 'main/userprofile_form.html'
    
    def get_object(self):
        if self.request.user.is_authenticated == False:
            return None

        User = self.request.user
        Profiles = UserProfile.objects.filter(id = User.id)
        if Profiles.count() == 0:
            Profile = UserProfile()
            Profile.id = User.id
            Profile.email = User.email
            Profile.first_name = User.first_name
            Profile.last_name = User.last_name
            Profile.save()
            return Profile
        else:
            return Profiles[0]


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)