from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm, UserProfileForm, UserForm
from .models import UserProfile

# Create your views here.

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('home') 
    else:
        form = SignupForm()
        
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

# login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'users/profile.html', context)

# def edit_profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = UserProfileForm(instance=user)
    
#     context = {'form': form}
#     return render(request, 'users/profile-edit.html', context)

# def edit_profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = UserProfileForm(instance=user_profile)
    
#     context = {'form': form}
#     return render(request, 'users/profile-edit.html', context)

def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'users/profile-edit.html', context)