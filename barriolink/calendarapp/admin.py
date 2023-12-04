from django.contrib import admin
from .models import Reservation, ReservationMember

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = [
        "id",
        "community_space",
        "user",
        "start_date_time",
        "end_date_time",
        "reservation_status",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
        "is_validated"
    ]
    list_filter = ["is_active", "is_deleted", "community_space"]
    search_fields = ["user__username"]

@admin.register(ReservationMember)
class ReservationMemberAdmin(admin.ModelAdmin):
    model = ReservationMember
    list_display = ["id", "reservation", "user", "created_at", "updated_at"]
    list_filter = ["reservation"]