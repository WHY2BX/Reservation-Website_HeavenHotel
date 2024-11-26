from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.views import View
from .forms import RegisterForm, PasswordChangeForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, Group


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)

            if request.user.is_staff:
                return redirect('bookingList')
            else:
                return redirect('mainpage')
        return render(request,'login.html', {"form":form})


class LogoutView(View):
    def get(self, request):
        logout(request) #clear session
        return render(request,'homepage.html')
    
 
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()  
        context = {  
            'form':form  
        }  
        return render(request, 'register.html', context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        # ตรวจว่ากรอกมาถูกไหม
        if form.is_valid():  
            form.save() 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
    
            # ตรวจว่ามี username, password ใน DB ไหม
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                view_bookings = Permission.objects.get(codename='view_bookings')
                delete_bookings = Permission.objects.get(codename='delete_bookings')
                add_bookings = Permission.objects.get(codename='add_bookings')
                view_rooms = Permission.objects.get(codename='view_rooms')
                
                user.user_permissions.add(view_bookings)
                user.user_permissions.add(delete_bookings)
                user.user_permissions.add(add_bookings)
                user.user_permissions.add(view_rooms)
                
                messages.success(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.error(request, 'There was a problem with your registration.')
            return render(request, 'register.html', {'form': form})

class PasswordChangeView(View):

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):          
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            return render(request, 'change_password.html', {'form': form})