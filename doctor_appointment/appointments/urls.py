from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TimeSlotViewSet,
    AvailabilityViewSet,
    AppointmentViewSet,
    DoctorRegistrationViewSet,
    PatientRegistrationViewSet,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r"timeslots", TimeSlotViewSet)
router.register(r"availabilities", AvailabilityViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(
    r"register_doctor", DoctorRegistrationViewSet, basename="doctor-registration"
)
router.register(
    r"register_patient", PatientRegistrationViewSet, basename="patient-registration"
)

urlpatterns = [
    path("", include(router.urls)),
    path("api/token_refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token_verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token_obtain/", TokenObtainPairView.as_view(), name="token_obtain"),
]
