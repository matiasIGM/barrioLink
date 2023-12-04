from django.forms import ModelForm, DateInput
from calendarapp.models import Reservation, ReservationMember
from django import forms

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ["community_space", "user", "start_date_time", "end_date_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "community_space": forms.Select(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),
            "start_date_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        
        }
        exclude = ["is_active", "is_deleted", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_date_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_date_time"].input_formats = ("%Y-%m-%dT%H:%M",)

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = ReservationMember
        fields = ["user"]

