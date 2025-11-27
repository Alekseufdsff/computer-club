from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'admin'

def is_intern(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'intern'

def index(request):
    news = News.objects.all().order_by('-created_at')[:5]
    return render(request, 'index.html', {'news': news})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def computers_list(request):
    computers = Computer.objects.filter(is_public=True)
    return render(request, 'computers/list.html', {'computers': computers})

@login_required
def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    return render(request, 'computers/detail.html', {'computer': computer})

@login_required
def request_computer(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        ComputerRequest.objects.create(
            user=request.user,
            computer=computer,
            message=message
        )
        messages.success(request, 'Заявка отправлена администратору!')
        return redirect('computers_list')
    return render(request, 'computers/request.html', {'computer': computer})

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    computers = Computer.objects.all()
    news = News.objects.all()
    tariffs = Tariff.objects.all()
    intern_tasks = InternTask.objects.all()
    requests = ComputerRequest.objects.filter(is_processed=False)
    
    return render(request, 'admin_panel/dashboard.html', {
        'users': users,
        'computers': computers,
        'news': news,
        'tariffs': tariffs,
        'intern_tasks': intern_tasks,
        'requests': requests,
    })

@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.role = new_role
        user_profile.save()
        messages.success(request, 'Роль пользователя обновлена!')
        return redirect('admin_users')
    return render(request, 'admin_panel/users.html', {'users': users})

@user_passes_test(is_admin)
def admin_computers(request):
    computers = Computer.objects.all()
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            computer = form.save(commit=False)
            computer.owner = request.user
            computer.save()
            messages.success(request, 'Компьютер добавлен!')
            return redirect('admin_computers')
    else:
        form = ComputerForm()
    return render(request, 'admin_panel/computers.html', {
        'computers': computers,
        'form': form
    })

@user_passes_test(is_admin)
def admin_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость добавлена!')
            return redirect('admin_news')
    else:
        form = NewsForm()
    news = News.objects.all()
    return render(request, 'admin_panel/news.html', {
        'news': news,
        'form': form
    })

@user_passes_test(is_admin)
def admin_tariffs(request):
    if request.method == 'POST':
        form = TariffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тариф добавлен!')
            return redirect('admin_tariffs')
    else:
        form = TariffForm()
    tariffs = Tariff.objects.all()
    return render(request, 'admin_panel/tariffs.html', {
        'tariffs': tariffs,
        'form': form
    })

@user_passes_test(is_admin)
def admin_interns(request):
    interns = User.objects.filter(userprofile__role='intern')
    if request.method == 'POST':
        form = InternTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задание добавлено!')
            return redirect('admin_interns')
    else:
        form = InternTaskForm()
    tasks = InternTask.objects.all()
    return render(request, 'admin_panel/interns.html', {
        'interns': interns,
        'tasks': tasks,
        'form': form
    })

@user_passes_test(is_admin)
def process_request(request, request_id):
    computer_request = get_object_or_404(ComputerRequest, id=request_id)
    if request.method == 'POST':
        contact_link = request.POST.get('contact_link')
        computer_request.contact_link = contact_link
        computer_request.is_processed = True
        computer_request.save()
        messages.success(request, 'Заявка обработана!')
    return redirect('admin_dashboard')