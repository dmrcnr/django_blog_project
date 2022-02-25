from django.shortcuts import render,redirect
from matplotlib.style import context
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
# Create your views here.


def register(request):
  
    form = RegisterForm(request.POST or None) #POST olursa form = RegisterForm(request.POST), POST olmazsa form = Register.Form() şeklinde boş oluşacak.
    
    if form.is_valid(): #Boş gelirse bu if durumuna girmeyecek.
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
           
        newUser = User(username =username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.success(request,"Başarıyla Kayıt Oldunuz.")
        return redirect("index")
    context = {
        "form" : form
    }
    return render(request,"register.html",context)

def user_login(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request,"Kullanıcı adı / Parola hatalı")
            return render(request,"login.html",context)

        messages.success(request,"Başarıyla Giriş Yapıldı.")
        login(request,user)
        return redirect("index")

    return render(request,"login.html",context)

def user_logout(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız.")
    return redirect("index")

