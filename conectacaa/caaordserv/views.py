from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'caaordserv/index.html')

def add_ordem(request):
    return render(request,'caaordserv/add_ordem.html')
