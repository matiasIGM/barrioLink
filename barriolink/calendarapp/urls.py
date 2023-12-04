from django.contrib import admin
from django.urls import path
from . import views  
 
app_name = "calendarapp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userReservation/', views.get_user_reservations, name='user_reservation'),
     path('adminReservations/', views.get_all_reservations, name='admin_reservations'),
    path("calendar/", views.CalendarViewNew.as_view(), name="calendar"),
    path("calendars/", views.CalendarView.as_view(), name="calendars"),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('next_week_reservation/<int:reservation_id>/', views.next_week_reservation, name='next_week_reservation'),
    path('next_day_reservation/<int:reservation_id>/', views.next_day_reservation, name='next_day_reservation'),
    path("reservation/new/", views.create_reservation, name="reservation_new"),
    path("reservation/edit/<int:pk>/", views.ReservationEdit.as_view(), name="reservation_edit"),
    path("reservation/<int:reservation_id>/details/", views.reservation_details, name="reservation-detail"),
    path(
        "add_reservationmember/<int:reservation_id>",
        views.add_reservationmember,
        name="add_reservationmember",
    ),
    path(
        "reservation/<int:pk>/remove",
        views.ReservationMemberDeleteView.as_view(),
        name="remove_reservation",
    ),
    path("all-reservation-list/", views.AllReservationsListView.as_view(), name="all_reservations"),
    path(
        "active-reservation-list/",
        views.ActiveReservationsListView.as_view(),
        name="active_reservations",
    ),
]