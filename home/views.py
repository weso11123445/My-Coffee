from django.shortcuts import render
from products.models import Product
# Create your views here.
def home(request):
    product = Product.objects.all()
    context = {'products':product}

    return render(request, 'index.html',context)


def about(request):

    return render(request , 'about.html')


def coffee(request):

    return render(request , 'coffee.html')