from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import requests

# Create your views here.

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            return redirect('home')
    else:
        form= UserCreationForm()
    return render(request, 'register.html', {'form':form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form' : form})                
            
     
def logout_page(request):
    logout(request)
    return redirect('login')

                    
    
        
    
    