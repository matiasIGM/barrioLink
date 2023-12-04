from django.db import models
from main.models import CustomUser, CommunitySpace
from datetime import datetime
from django.urls import reverse

# Create your models here.
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    community_spacea = models.ForeignKey(CommunitySpace, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    reservation_status = models.CharField(max_length=20)



class ReservationAbstract(models.Model):
    """ Reservation abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_validated = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ReservationMember(ReservationAbstract):
    """ Reservation member model """

    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="reservations")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reservation_members"
    )

    class Meta:
        unique_together = ["reservation", "user"]

    def __str__(self):
        return str(self.user)


class ReservationManager(models.Manager):
    """ Reservation manager """

    def get_all_reservations(self, user):
        reservations = Reservation.objects.filter(user=user, is_active=True, is_deleted=False)
        return reservations

    def get_active_reservations(self, user):
        active_reservations = Reservation.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_date_time__gte=datetime.now().date(),
        ).order_by("start_date_time")
        return active_reservations


class Reservation(ReservationAbstract):
    """ Reservation model """

    community_space = models.ForeignKey(CommunitySpace, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    reservation_status = models.CharField(max_length=20, blank=True)

    objects = ReservationManager()

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("calendarapp:reservation-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:reservation-detail", args=(self.id,))
        return f'<a href="{url}">Reservation {self.id}</a>'
    
    @property
    def duration_in_days(self):
        # Calcular la duración en días
        duration = self.end_date_time - self.start_date_time
        return duration.days