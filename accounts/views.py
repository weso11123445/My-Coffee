from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
import re
from django.contrib import auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from products.models import Product


# Create your views here.
def signin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username , password=password)

        if user is not None:
            if 'rememmber' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
            messages.success(request,'You are Now Loggen in')
        else:
            messages.error(request,'username or password is not Valid')

    return render(request, 'signin.html')


def signup(request):
    fname = ''
    lname = ''
    address = ''
    address2 = ''
    city = ''
    state = ''
    zip_number = ''
    email = ''
    username = ''
    password = ''
    terms = ''
    is_added = ''

    if request.POST:

        if 'fname' in request.POST:
            fname = request.POST['fname']
        else:
            messages.ERROR(request , 'Error in first name')
        if 'lname' in request.POST:
            lname = request.POST['lname']
        else:
            messages.error(request , 'Error in Last Name')
        if 'address' in request.POST:
            address = request.POST['address']
        else:
            messages.error(request,'Error in address')
        if 'address2' in request.POST:
            address2 = request.POST['address2']
        else:
            messages.error(request,'error in address2')
        if 'city' in request.POST:
            city = request.POST['city']
        else:
            messages.error(request,'error in city')
        if 'state' in request.POST:
            state = request.POST['state']
        else:
            messages.error(request,'error in stata')
        if 'zip' in request.POST:
            zip_number = request.POST['zip']
        else:
            messages.error(request,'error in zip_number')
        if 'username' in request.POST:
            username=request.POST['username']
        else:
            messages.error(request,'error in username')
        if 'password' in request.POST:
            password=request.POST['password']
        else:
            messages.error(request,'error in password')
        if 'email' in request.POST:
            email = request.POST['email']
        else:
            messages.error(request,'error in email')
        if 'terms' in request.POST:
            terms = request.POST['terms']


        if fname and lname and address and address2 and city and state  and zip_number and username and email and password:
            if terms == 'on':
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username is found please enter anoher username')
                else:

                    if User.objects.filter(email=email).exists():
                        messages.error(request,'your email is taken')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt , email):
                            user = User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
                            user.save()
                            userprofile = UserProfile(user=user , address=address ,address2=address2,city=city,state=state,zip_number=zip_number)
                            userprofile.save()
                            fname=''
                            lname=''
                            address=''
                            address2=''
                            state=''
                            city = ''
                            zip_number=''
                            username=''
                            password=''
                            email=''
                            terms=None
                            messages.success(request,'Your Account is Created')
                            is_added = True

                        else:
                            messages.error(request,'invalid email')

            else:
                messages.error(request,'you Must Agree on Terms')
        else:
            messages.error(request,'Check Empty Field')

    context = {'fname':fname ,'lname':lname, 'address':address,'address2':address2,
                   'city':city , 'state':state, 'email':email,'user':username,'pass':password,'zip':zip_number,
                   'is_added':is_added
                   }


    return render(request, 'signup.html',context)

def profile(request):
    if request.user is not None:
        context = None

        if not request.user.is_anonymous:
            userprofile = UserProfile.objects.get(user=request.user)
            if 'btnprofile' in request.POST:
                if request.POST['fname'] and request.POST['lname'] and request.POST['email'] and request.POST['username']and request.POST['password'] and request.POST['address'] and request.POST['address2'] and request.POST['state']and request.POST['city'] and request.POST['zip'] :
                    request.user.first_name = request.POST['fname']
                    request.user.last_name = request.POST['lname']
                   # request.user.email = request.POST['email']
                   # request.user.username = request.POST['username']
                    if not request.POST['password'].startswith('pbkdf2_sha256'):
                        request.user.set_password(request.POST['password'])
                   #request.user.password = request.POST['password']
                    userprofile.address = request.POST['address']
                    userprofile.address2 = request.POST['address2']
                    userprofile.state = request.POST['state']
                    userprofile.city = request.POST['city']
                    userprofile.zip_number = request.POST['zip']
                    request.user.save()
                    userprofile.save()
                    messages.success(request,'your Data has been Saved')
                else:
                    messages.error(request ,'check empty fields')

           #userprofile = UserProfile.objects.get(user=request.user)
            context = {'fname':request.user.first_name ,'lname':request.user.last_name,
                   'email':request.user.email, 'user':request.user.username,'pass':request.user.password,
                   'address':userprofile.address, 'address2':userprofile.address2,'city':userprofile.city,
                   'state':userprofile.state, 'zip_number':userprofile.zip_number,
                      }


        return render(request, 'profile.html',context)
    else:
        return render(request, 'profile.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('index')


def product_favorite(request , pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(product_favorites=pro_fav , user =request.user).exists():
            messages.success(request,'already Product in Favorite')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            userprofile.save()
            messages.success(request,'product has been added')


    else:
        messages.error(request,'you must login ')

    return redirect('/products/' + str(pro_id))

def show_product_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userinfo = UserProfile.objects.get(user=request.user)
        pro = userinfo.product_favorites.all()
        context = {'product':pro}





    return render(request,'products.html',context)
