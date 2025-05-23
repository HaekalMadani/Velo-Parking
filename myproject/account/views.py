from django.shortcuts import render

# Create your views here.
def login(request):
    context = {"a": "apple"}
    return render(request, 'account/login.html', context)
