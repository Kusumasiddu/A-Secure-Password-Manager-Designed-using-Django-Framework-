from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import PasswordForm
from .models import Password, Notification

def home_page(request):
    return render(request, 'pw_storage/home.html')


def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home-page')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('password-list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('login-page')


# ----------------------------------------------------------
# FIXED PASSWORD LIST (Only one version kept)
# ----------------------------------------------------------
@login_required
def password_list(request):
    query = request.GET.get('q')
    search_active = False

    if query:
        passwords = Password.objects.filter(
            user=request.user,
            name__icontains=query
        )
        search_active = True
    else:
        passwords = Password.objects.filter(user=request.user)

    return render(request, 'pw_storage/password_list.html', {
        'passwords': passwords,
        'query': query,
        'search_active': search_active,
    })


@login_required
def add_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.save(commit=False)
            password.user = request.user
            password.save()
            return redirect('password-list')
    else:
        form = PasswordForm()
    return render(request, 'pw_storage/add_password.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Password
from .forms import PasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def update_password(request, id):
    password = get_object_or_404(Password, id=id, user=request.user)

    if request.method == "POST":
        form = PasswordForm(request.POST, request.FILES, instance=password)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully!")
            return redirect('password-list')
    else:
        form = PasswordForm(instance=password)

    return render(request, 'pw_storage/update_password.html', {
        'form': form,
        'password': password
    })


@login_required
def delete_password(request, id):
    password = get_object_or_404(Password, id=id, user=request.user)
    name = password.name
    password.delete()

    Notification.objects.create(
        user=request.user,
        action="Deleted password",
        password_name=name
    )
    return redirect('password-list')
