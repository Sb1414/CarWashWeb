import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Location, Booking
from .forms import RegistrationForm, BookingForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages\

def home(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/home.html', {'form': form})

def about(request):
    services = Service.objects.all()
    locations = Location.objects.all()
    locations_data = json.dumps([
        {
            'city': location.city,
            'address': location.address,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude)
        }
        for location in locations
    ])
    return render(request, 'main/about.html', {'services': services, 'locations': locations, 'locations_data': locations_data})



def contacts_view(request):
    locations = Location.objects.all()
    locations_data = json.dumps([
        {
            'city': location.city,
            'address': location.address,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude)
        }
        for location in locations
    ])
    return render(request, 'main/contacts.html', {'locations': locations, 'locations_data': locations_data})

def services(request):
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})


@login_required
def book_service(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Сохранение заказа в базе данных
            booking = Booking(
                service=service,
                user=request.user,
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time']
            )
            booking.save()

            messages.success(request, 'Ваша заявка успешно принята и находится на рассмотрении.')

            return redirect('services')  # Замените на нужный URL
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Попробуйте еще раз.')
    else:
        form = BookingForm()

    return render(request, 'main/book_service.html', {'service': service, 'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно. Вы можете войти.')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'main/my_bookings.html', {'bookings': bookings})


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно обновлена.")
            return redirect('my_bookings')
        else:
            messages.error(request, "Ошибка при обновлении заявки.")
    else:
        form = BookingForm(instance=booking)

    return render(request, 'main/edit_booking.html', {'form': form, 'booking': booking})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Заявка успешно удалена.")
        return redirect('my_bookings')

    return render(request, 'main/delete_booking_confirm.html', {'booking': booking})