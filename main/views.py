import json
from typing import io

import qrcode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Location, Booking, Specialist, Slot
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
    specialists = Specialist.objects.prefetch_related('services').all()
    return render(request, 'main/services.html', {'specialists': specialists})


@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    available_slots = Slot.objects.filter(service=service, is_booked=False).order_by('date', 'time')

    if request.method == "POST":
        slot_id = request.POST.get('slot')
        if slot_id:
            slot = Slot.objects.get(id=slot_id)
            if not slot.is_booked:
                Booking.objects.create(
                    service=service,
                    user=request.user,
                    date=slot.date,
                    time=slot.time
                )
                slot.is_booked = True
                slot.save()
                messages.success(request, "Вы успешно записались на услугу!")
                return redirect('my_bookings')
            else:
                messages.error(request, "Этот слот уже забронирован. Пожалуйста, выберите другой.")
        else:
            messages.error(request, "Выберите слот для записи.")

    return render(request, 'main/book_service.html', {'service': service, 'slots': available_slots})


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

@login_required
def my_slots(request):
    try:
        specialist = Specialist.objects.get(user=request.user)
    except Specialist.DoesNotExist:
        messages.error(request, "Вы не являетесь специалистом.")
        return redirect('services')

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')

        if date and time:
            Slot.objects.create(specialist=specialist, date=date, time=time)
            messages.success(request, "Слот успешно добавлен!")
        else:
            messages.error(request, "Укажите корректные дату и время.")

    slots = Slot.objects.filter(specialist=specialist).order_by('date', 'time')
    return render(request, 'main/my_slots.html', {'slots': slots})


def payment_qr(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Генерация ссылки для СБП
    sbp_url = f"bank://qr/?payee=41001100100&sum={booking.service.price}&paymentPurpose={booking.service.name}"

    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(sbp_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")

@login_required
def payment_redirect(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    payee = "41001100100"
    amount = booking.service.price
    purpose = f"Оплата услуги: {booking.service.name}"
    sbp_url = f"bank://qr/?payee={payee}&sum={amount}&paymentPurpose={purpose}"

    return render(request, 'main/payment_redirect.html', {
        'sbp_url': sbp_url,
        'booking': booking
    })