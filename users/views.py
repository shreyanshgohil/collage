from django.shortcuts import redirect, render
from store.models import Cart, CartItem
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from store.views import _cart_id


# Create your views here.

def user_register(request):
    if not request.user.is_authenticated:
        form = CreateUserForm()
        if request.method == 'POST':
            form =CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                uname = form.cleaned_data.get("username")
                email =  form.cleaned_data.get("email")
                
                #seting is_active to false

                user = User.objects.get(username  = uname)
                # print(user)
                #for send mail
                subject = 'Welcome to Outfut Manager Mr/Miss '+uname
                message = 'We are glad you are here!'

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                #end of sending mail
                messages.success(request,"account created with username: "+uname)
                return redirect('login')
        
        
        context = {'form':form}
        return render(request,'users/register.html',context)
    else:
        return redirect('store')

def user_login(request):
    if not request.user.is_authenticated: 
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(username,password)

            try:
                user = User.objects.get(username=username)
            except:
                messages.warning(request,'username dose not match ')

            user = authenticate(request,username = username,password = password)
            if user is not None:
                
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_iteams = CartItem.objects.filter(cart=cart)
                except:
                    pass
                login(request, user)
                try:
                    for cart_iteam in cart_iteams:
                        cart_iteam.user = user
                        cart_iteam.save()
                except:
                    pass
                messages.success(request,'Login Done Successfully')
                return redirect('home')
            else:
                messages.warning(request,"username or password is incorrect")
        return render(request,'users/login.html')
    else:
        return redirect('store')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request,"User Logout Successfully")
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'users/dashboard.html')

