from rest_framework import serializers
from .models import CustomUser, Doctor, Patient, TimeSlot, Availability, Appointment
from django.contrib.auth.hashers import make_password


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"


class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Availability
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def post(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Doctor
        fields = ["user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserRegistrationSerializer.create(
            UserRegistrationSerializer(), validated_data=user_data
        )
        user.is_doctor = True
        user_password = make_password(user.password)
        user.password = user_password
        user.save()
        doctor = Doctor.objects.create(user=user)
        return doctor


class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Patient
        fields = ["user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserRegistrationSerializer.create(
            UserRegistrationSerializer(), validated_data=user_data
        )
        user.is_patient = True
        user_password = make_password(user.password)
        user.password = user_password
        user.save()
        patient = Patient.objects.create(user=user)
        return patient
