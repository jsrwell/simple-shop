from django.shortcuts import render


def home(request):
    context = {'message': 'Hello from Django!'}
    return render(request, 'pages/home.html', context)
