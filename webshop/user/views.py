from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms import UserForm
from .models import UserProfile
from .forms import SignupForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from products.models import Product


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


@login_required
def profile(request):
    user = request.user
    created_products = Product.objects.filter(created_by=user)
    return render(request, 'users/profile.html', {'user': user, 'created_products': created_products})


def custom_logout(request):
    logout(request)
    return redirect('home')


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
