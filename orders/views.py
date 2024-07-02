from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Order , OrderDetails , Payment
from products.models import Product
from django.utils import timezone
from django.contrib.auth.models import User


# Create your views here.

def add_to_cart(request):

    if 'pro_id' in request.GET and 'quantity' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        if request.GET['quantity'] == '':
            messages.error(request,'Please Inter A number')
            return redirect('/products/' + request.GET['pro_id'])
        if int(request.GET['quantity']) > 0 :
            pro_id = request.GET['pro_id']
            qty = request.GET['quantity']

            order = Order.objects.all().filter(user=request.user, is_finished=False)
            pro = Product.objects.get(id=pro_id)

            if order:

                old_order = Order.objects.get(user=request.user,is_finished=False)
                if OrderDetails.objects.all().filter(order=old_order,product=pro_id).exists():
                    orderdetails = OrderDetails.objects.get(order=old_order,product=pro_id)
                    orderdetails.quantity += int(qty)
                    orderdetails.save()
                else:

                    orderdetails = OrderDetails.objects.create(product=pro,order=old_order,price=pro.price,quantity=qty)
                messages.success(request, 'Was added to Card for old order')


            else:
                messages.success(request,'here we will make a new Order')
                new_order = Order()
                new_order.user = request.user
                new_order.order_date = timezone.now()
                new_order.is_finished = False
                new_order.save()
                orderdetails = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty)





        else:
            messages.error(request,'you must inter an integer value ')

        return redirect('/products/' + request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request,'You Must Be Logged in')
            return redirect('/products/' + request.GET['pro_id'])
        #return redirect('products')
        else:
            return redirect('index')

def show_cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order = Order.objects.get(user=request.user,is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for sum in orderdetails:
                total += sum.price * sum.quantity

            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
            }


    return render(request,'cart.html',context)

def remove_from_cart(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.delete()



    return redirect('show_cart')

def add_qty(request,orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.quantity += 1
            orderdetails.save()


    return redirect('show_cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            if orderdetails.quantity > 1 :
                orderdetails.quantity -= 1
                orderdetails.save()

    return redirect('show_cart')



def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    expire = None
    security_code = None
    is_added = None

    if request.method=='POST' and 'btnpayment' in request.POST and 'ship_address' in request.POST and 'ship_phone' in request.POST \
            and 'card_number' in request.POST and 'expire' in request.POST and 'security_code' in request.POST:
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        expire = request.POST['expire']
        security_code = request.POST['security_code']

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                payment = Payment(order=order,shipment_address=ship_address,
                                  shipment_phone=ship_phone,card_number=card_number,
                                  expire=expire,security_code=security_code)
                payment.save()
                order.is_finished = True
                order.save()
                is_added = True
                messages.success(request,'your order is finished')




        context = {
            'ship_address':ship_address,
            'ship_phone':ship_phone,
            'card_number':card_number,
            'expire':expire ,
            'security_code':security_code,
            'is_added':is_added,
        }

    else:

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for sum in orderdetails:
                    total += sum.price * sum.quantity

                context = {
                    'order': order,
                    'orderdetails': orderdetails,
                    'total': total,
                }


    return render(request , 'payment.html', context)

def show_orders(request):
    context=None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
            all_orders = Order.objects.all().filter(user=request.user)
         #   if all_orders:
          #      order = Order.objects.get(user=request.user, is_finished=False)
           #     orderdetails = OrderDetails.objects.all().filter(order=order)
            #    total = 0
             #   for sum in orderdetails:
              #      total += sum.price * sum.quantity

    context = {'all_orders': all_orders}

    return render(request, 'show_orders.html', context)