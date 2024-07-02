from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
# Create your views here.

def product(request,pro_id):
    product = get_object_or_404(Product, pk=pro_id)
    context = {'product':product}

    return render(request,'product.html',context)


def products(request):
    pro = Product.objects.all()
    name1 = None
    pfrom = None
    pto = None
    cs=None
    if 'cs' in request.GET:
        cs = request.GET['cs']

    if 'searchname' in request.GET:
           name = request.GET['searchname']
           if name:
               pro = pro.filter(name__icontains=name)

    if 'desc' in request.GET:
        desc = request.GET['desc']
        if desc:
            pro =pro.filter(description__icontains=desc)

    if 'pricefrom' in request.GET and 'priceto' in request.GET:
        pfrom = request.GET['pricefrom']
        pto = request.GET['priceto']

        if pfrom.isdigit() and pto.isdigit():
            pro = pro.filter(price__gte=pfrom , price__lte=pto)


    context = {'product': pro }

    return render(request , 'products.html' ,context)

def search(request):


    return render(request, 'search.html')