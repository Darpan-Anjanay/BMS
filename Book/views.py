from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

@login_required(login_url='Login')
def Home(request):
    return render(request,'BK/Home.html')

@login_required(login_url='Login')
def  Admin(request):
    if  request.user.is_superuser:

            
        users =  User.objects.all()
        print(users.values())
        context = {'users':users}
        return render(request,'BK/Admin.html',context)
    else:
        return redirect('Home')



def Login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            messages.info(request,'Invalid Creadentails')

           
    return render(request,'BK/Login.html')

@login_required(login_url='Login')
def Logout(request):
    logout(request)
    return redirect('Login')