from django.shortcuts import render

def home(request):
    return render(request, 'main/index.html', 
    {
        'turn_on_block': True,
        'username': request.user.username, 
    })
