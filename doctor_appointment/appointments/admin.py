from django.contrib import admin
from .models import CustomUser, Doctor, Patient, TimeSlot, Availability, Appointment

admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(TimeSlot)
admin.site.register(Availability)
admin.site.register(Appointment)
