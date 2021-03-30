from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

from main.models import Good

def home(request):
    """ Возвращает главную страницу сайта """
    return render(request, 'main/index.html', 
    {
        'turn_on_block': True,
        'username': request.user.username, 
    })

class GoodListView(ListView):
    """ Представление списка товаров """
    context_object_name = 'object_list'
    queryset = Good.objects.all()
    template_name = 'main/good_list.html'

    def get_queryset(self):
        return Good.objects.order_by('name')


class GoodDetailView(DetailView):
    """ Представление товара """
    model = Good
