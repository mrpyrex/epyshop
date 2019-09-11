from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            register_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(register_user)
            messages.success(
                request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
