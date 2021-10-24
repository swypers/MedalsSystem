from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'home.html', {})



def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(), password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        redirict_path = next_ or next_post or '/'
        return redirect(redirict_path)
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm(request.POST or None)
        return render(request, 'register.html', {'form': user_form})
