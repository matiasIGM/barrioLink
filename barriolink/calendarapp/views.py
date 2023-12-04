from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from calendarapp.models import ReservationMember, Reservation
from main.models import CommunitySpace
from calendarapp.utils import Calendar
from calendarapp.forms import ReservationForm, AddMemberForm
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
import json
import random
import string

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Reservation
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context

@login_required(login_url="signup")
def create_reservation(request):
    form = ReservationForm(request.POST or None)
    if request.POST and form.is_valid():
        community_space = form.cleaned_data["community_space"]
        user = form.cleaned_data["user"]
        start_date_time = form.cleaned_data["start_date_time"]
        end_date_time = form.cleaned_data["end_date_time"]
        reservation_status = form.cleaned_data["reservation_status"]
        Reservation.objects.get_or_create(
            user=user,
            community_space=community_space,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            reservation_status=reservation_status,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "reservation.html", {"form": form})

class ReservationEdit(generic.UpdateView):
    model = Reservation
    fields = ["community_space", "user", "start_date_time", "end_date_time", "reservation_status"]
    template_name = "reservation.html"

@login_required(login_url="signup")
def reservation_details(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservationmember = ReservationMember.objects.filter(reservation=reservation)
    context = {"reservation": reservation, "reservationmember": reservationmember}
    return render(request, "reservation-details.html", context)

def add_reservationmember(request, reservation_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = ReservationMember.objects.filter(reservation=reservation_id)
            reservation = Reservation.objects.get(id=reservation_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                ReservationMember.objects.create(reservation=reservation, user=user)
                return redirect("calendarapp:calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)

class ReservationMemberDeleteView(generic.DeleteView):
    model = ReservationMember
    template_name = "reservation_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = ReservationForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        reservations = Reservation.objects.get_all_reservations(user=request.user)
        active_reservations = Reservation.objects.get_active_reservations(user=request.user)
        reservation_list = []

        for reservation in reservations:
            reservation_list.append(
                {
                    "id": reservation.id,
                    "title": f"Reservation {reservation.id}",
                    "start": reservation.start_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": reservation.end_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "description": reservation.reservation_status,
                }
            )
        
        context = {"form": forms, "reservations": reservation_list, "active_reservations": active_reservations}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return JsonResponse({'message': 'Reservation successfully deleted.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_week_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        next_reservation = reservation
        next_reservation.id = None
        next_reservation.start_date_time += timedelta(weeks=1)
        next_reservation.end_date_time += timedelta(weeks=1)
        next_reservation.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        next_reservation = reservation
        next_reservation.id = None
        next_reservation.start_date_time += timedelta(days=1)
        next_reservation.end_date_time += timedelta(days=1)
        next_reservation.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

class AllReservationsListView(ListView):
    """ All reservation list views """

    template_name = "calendarapp/reservations_list.html"
    model = Reservation

    def get_queryset(self):
        return Reservation.objects.get_all_reservations(user=self.request.user)

class ActiveReservationsListView(ListView):
    """ Active reservations list view """

    template_name = "account/users/reservations.html"
    model = Reservation

    def get_queryset(self):
        # Devuelve todas las reservas del usuario actualmente autenticado
        reservations = Reservation.objects.filter(user=self.request.user)
        return reservations
    
    def get_context_data(self, **kwargs):
        # Llamamos al método get_context_data de la clase padre
        context = super().get_context_data(**kwargs)

        # Obtener solo el campo "reservation_status" de cada reserva
        reservation_statuses = [reservation.reservation_status for reservation in context['object_list']]

        # Agregar la variable al contexto
        context['reservation_statuses'] = reservation_statuses

        return context
    
def generate_random_color():
    # Generar un código de color hexadecimal aleatorio
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color


def get_user_reservations(request):
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener los nombres de los espacios comunitarios de las reservas del usuario actual
        community_space_names = (
            CommunitySpace.objects
            .filter(reservation__user=request.user)
            .values_list('name', flat=True)
        )

        # Obtener todas las reservas activas del usuario
        user_reservations = []
        for reservation in Reservation.objects.filter(user=request.user, is_active=True):
            reservation_data = {
                'title': reservation.community_space.name,
                'start': reservation.start_date_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Convertir a cadena con formato ISO
                'end': reservation.end_date_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Convertir a cadena con formato ISO
                'color': generate_random_color()
            }
            user_reservations.append(reservation_data)

        # Convertir la QuerySets a listas para facilitar la serialización a JSON
        community_space_names_list = list(community_space_names)
        user_reservations_list = list(user_reservations)
        
         # Pasa los datos al contexto
        context = {
            'community_space_names': community_space_names_list,
            'user_reservations': user_reservations_list,
        }

        # Devolver los datos en formato JSON
        json_data = {'community_space_names': community_space_names_list, 'user_reservations': user_reservations_list}
        
        # Verificar si la solicitud es una solicitud AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(json_data)
        else:
            # Pasa los datos al contexto como una cadena JSON
            context = {
                'community_space_names': community_space_names_list,
                'user_reservations': user_reservations_list,
                'json_data': json.dumps(json_data),  # Convertir a cadena JSON
        }
            
        return render(request, 'account/users/reservations.html',  context)
    else:
        # Usuario no autenticado, redirigir o manejar de acuerdo a tus necesidades
        return render(request, 'account/users/reservations.html')
    
    


def get_all_reservations(request):
    # Obtener todas las reservas
    all_reservations = Reservation.objects.all()

    # Guardar las reservas en el contexto
    context = {'reservations': all_reservations}

    # Renderizar la plantilla con el contexto
    return render(request, 'account/adm/reservations.html', context)