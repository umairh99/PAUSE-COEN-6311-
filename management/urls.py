from django.urls import path
from .views import AgencyView, FlightView, HotelView, ActivityView, ImageUpload, HomeView, \
    FlightsView, HotelsView, ActivitiesView, PackageView, PackagesView, CustomPackageView, \
    BookingView, BookingsView, PaymentView, SuccessView, SearchView
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

router = DefaultRouter()

router.register(r'manage/flights', FlightView, basename='flight')
router.register(r'manage/hotels', HotelView, basename='hotel')
router.register(r'manage/activities', ActivityView, basename='acitivity')
router.register(r'manage/packages', PackageView, basename='package')
router.register(r'manage/bookings', BookingsView, basename='booking')
router.register(r'flights', FlightsView, basename='flights')
router.register(r'hotels', HotelsView, basename='hotels')
router.register(r'activities', ActivitiesView, basename='activities')
router.register(r'packages', PackagesView, basename='packages')
router.register(r'my-packages', CustomPackageView, basename='cpackages')
router.register(r'my-bookings', BookingView, basename='mbookings')

urlpatterns = [
    path('', HomeView.as_view()),
    path('manage/agency/', AgencyView.as_view()),
    path('manage/image/', ImageUpload.as_view()),
    path('payment/', PaymentView.as_view()),
    path('cancel/', TemplateView.as_view(template_name='cancel.html')),
    path('success/<int:id>/', SuccessView.as_view()),
    path('search/', SearchView.as_view())
] + router.urls
