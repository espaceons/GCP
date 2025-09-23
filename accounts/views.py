from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST, request.FILES)
#         profile_form = UserProfileForm(request.POST)
#         if form.is_valid() and profile_form.is_valid():
#             user = form.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = RegistrationForm()
#         profile_form = UserProfileForm()
#     return render(request, 'accounts/register.html', {'form': form, 'profile_form': profile_form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # cree un profil utilisateur
            UserProfile.objects.create(user=user)
            # connecter l'utilisateur automatiquement
            login(request, user)

            return redirect('home')

        else:
            form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# @login_required
# def profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, instance=user_profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect('profile')
#     else:
#         profile_form = UserProfileForm(instance=user_profile)

#     return render(request, 'accounts/profile.html', {'profile_form': profile_form})


@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'profile_form': profile_form, 'user': user})


@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'profile_form': profile_form, 'user': user})


@login_required
def dashboard(request):
    return render(request, 'home.html')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')
