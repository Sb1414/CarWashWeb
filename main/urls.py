from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/book/', views.book_service, name='book_service'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('my_slots/', views.my_slots, name='my_slots'),
    path('payment/<int:booking_id>/', views.payment_qr, name='payment_qr'),
    path('payment_redirect/<int:booking_id>/', views.payment_redirect, name='payment_redirect'),
    path('activate_camera/<int:slot_id>/', views.activate_camera, name='activate_camera'),
    path('toggle_camera/<int:slot_id>/', views.toggle_camera, name='toggle_camera'),
    path('complete_service/<int:slot_id>/', views.complete_service, name='complete_service'),
]
