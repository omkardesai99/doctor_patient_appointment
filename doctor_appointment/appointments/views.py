from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Doctor, Patient, TimeSlot, Availability, Appointment
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    CustomUserSerializer,
    TimeSlotSerializer,
    AvailabilitySerializer,
    AppointmentSerializer,
    DoctorRegistrationSerializer,
    PatientRegistrationSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from appointments.permission import IsDoctorOrReadOnly
from rest_framework.decorators import action


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


# class AvailabilityViewSet(viewsets.ModelViewSet):
#     queryset = Availability.objects.all()
#     serializer_class = AvailabilitySerializer

#     def create(self, request, *args, **kwargs):
#         doctor_id = request.data.get("doctor")
#         date = request.data.get("date")
#         time_slot_id = request.data.get("time_slot")

#         if Availability.objects.filter(
#             doctor_id=doctor_id, date=date, time_slot_id=time_slot_id
#         ).exists():
#             return Response(
#                 {"error": "Availability already exists for this doctor and time slot."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         time_slot = TimeSlot.objects.get(id=time_slot_id)
#         availability = Availability.objects.create(
#             doctor_id=doctor_id, date=date, time_slot=time_slot
#         )
#         availability.save()
#         return Response(
#             AvailabilitySerializer(availability).data, status=status.HTTP_201_CREATED
# )


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsDoctorOrReadOnly, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = (
            self.get_queryset()
            .filter(is_available=True)
            .order_by("date", "time_slot__start_time")
        )
        print(f"queryset: {[i.__dict__ for i in queryset]}")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_doctor:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Only doctors can create availability"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_doctor:
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Only doctors can update availability"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_doctor:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Only doctors can delete availability"},
                status=status.HTTP_403_FORBIDDEN,
            )


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get("patient")
        doctor_id = request.data.get("doctor")
        date = request.data.get("date")
        time_slot_id = request.data.get("time_slot")

        if not request.user.is_patient:
            return Response(
                {"error": "Only patients can create appointments."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if Appointment.objects.filter(
            patient_id=patient_id, date=date, time_slot_id=time_slot_id
        ).exists():
            return Response(
                {"error": "Patient already has an appointment at this time"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Appointment.objects.filter(
            doctor_id=doctor_id, date=date, time_slot_id=time_slot_id
        ).exists():
            return Response(
                {"error": "Doctor already has an appointment at this time"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        availability = Availability.objects.filter(
            doctor_id=doctor_id, date=date, time_slot_id=time_slot_id, is_available=True
        ).first()

        if availability:
            appointment = Appointment.objects.create(
                patient_id=patient_id,
                doctor_id=doctor_id,
                date=date,
                time_slot_id=time_slot_id,
            )
            availability.is_available = False
            availability.save()
            return Response(
                AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "The requested time slot is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # curl -X DELETE  http://localhost:8000/api/appointments/4/
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_patient and instance.patient.user != request.user:
            return Response(
                {"error": "You do not have permission to cancel this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.is_doctor and instance.doctor.user != request.user:
            return Response(
                {"error": "You do not have permission to cancel this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        availability = Availability.objects.get(
            doctor_id=instance.doctor_id,
            date=instance.date,
            time_slot_id=instance.time_slot_id,
        )
        availability.is_available = True
        availability.save()

        self.perform_destroy(instance)
        return Response(
            {"message": "deleted succesfully"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        doctor_name = request.query_params.get("doctor", None)
        patient_name = request.query_params.get("patient", None)

        queryset = self.queryset

        if doctor_name:
            queryset = queryset.filter(doctor__user__username__icontains=doctor_name)
        if patient_name:
            queryset = queryset.filter(patient__user__username__icontains=patient_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# {
#   "user": {
#     "username": "doctor3",
#     "email": "doctor3@gmail.com",
#     "password": "123"
#   }
# }
class DoctorRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegistrationSerializer


# {
#   "user": {
#     "username": "patient3",
#     "email": "patient3@gmail.com",
#     "password": "123"
#   }
# }
class PatientRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientRegistrationSerializer
