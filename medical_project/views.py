from django.shortcuts import render

def home(request):
    return render(request, 'main_app/home.html')

def server1(request):
    return render(request, 'main_app/server1.html')

def server2(request):
    return render(request, 'main_app/server2.html')

def server3(request):
    return render(request, 'main_app/server3.html')

def server4(request):
    return render(request, 'main_app/server4.html')

def server5(request):
    return render(request, 'main_app/server5.html')
