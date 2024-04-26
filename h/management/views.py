from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView, CreateAPIView
from .models import Agency, Flight, Hotel, Activity, Photo, Package, CustomPackage, Booking, Payment
from .serializers import AgencySerializer, HotelSerializer, FlightSerializer, ActivitySerializer, ImageSerializer, \
    PackageGETSerializer, PackageCreateSerializer, CustomPackageSerializer, CustomPackageGet, mybookingget, mybookingser, \
    PaymentSerializier
from security.views import HybridViewMixin
from django.shortcuts import render, redirect
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q
import stripe


class AgencyView(
    HybridViewMixin, GenericAPIView, CreateModelMixin,
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
):
    serializer_class = AgencySerializer
    template_name = 'agency.html'

    def get_object(self):
        try:
            user = self.request.user
            return Agency.objects.select_related('agent').get(agent=user)
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def render_html(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {}
            if self.get_object() is not None:
                serializer = self.serializer_class(self.get_object())
                context = {**serializer.data}
            return render(request, self.template_name, context=context)
        else:
            return redirect('/account/login')


class BaseView(HybridViewMixin, viewsets.ModelViewSet):
    model = None
    list_template_name = None
    detail_template_name = None
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(agency__agent=user)

    def render_html(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.query_params = request.GET
            if kwargs.get('pk') is None:
                queryset = self.filter_queryset(self.get_queryset())
                serializer = queryset
                return render(request, self.list_template_name, context={'items': serializer})
            else:
                serializer = self.get_object()
                return render(request, self.detail_template_name, context={'item': serializer})
        else:
            return redirect('/account/login/')


class ImageUpload(CreateAPIView):
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            for image in serializer.validated_data['images']:
                obj = Photo.objects.create(img=image)
                obj.save()
                if serializer.validated_data.get('flight'):
                    instance = Flight.objects.get(
                        pk=serializer.validated_data['flight'])
                elif serializer.validated_data.get('hotel'):
                    instance = Hotel.objects.get(
                        pk=serializer.validated_data['hotel'])
                elif serializer.validated_data.get('activity'):
                    instance = Activity.objects.get(
                        pk=serializer.validated_data['activity'])
                instance.pictures.add(obj.id)
                instance.save()
        return Response()


class FlightView(BaseView):
    serializer_class = FlightSerializer
    model = Flight
    search_fields = ['airline', 'price']
    list_template_name = 'flightlist.html'
    detail_template_name = 'flightdetail.html'


class HotelView(BaseView):
    serializer_class = HotelSerializer
    model = Hotel
    search_fields = ['name', 'location', 'price_per_night']
    list_template_name = 'hotellist.html'
    detail_template_name = 'hoteldetail.html'


class ActivityView(BaseView):
    serializer_class = ActivitySerializer
    model = Activity
    search_fields = ['name', 'location', 'price']
    list_template_name = 'activitylist.html'
    detail_template_name = 'activitydetail.html'


class HomeView(TemplateView):
    template_name = 'dashboard.html'


class ReadonlyBaseView(HybridViewMixin, viewsets.ReadOnlyModelViewSet):
    model = None
    list_template_name = None
    detail_template_name = None
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]

    def render_html(self, request, *args, **kwargs):
        request.query_params = request.GET
        if kwargs.get('pk') is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = queryset
            return render(request, self.list_template_name, context={'items': serializer})
        else:
            serializer = self.get_object()
            return render(request, self.detail_template_name, context={'item': serializer})


class FlightsView(ReadonlyBaseView):
    model = Flight
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    search_fields = ['airline', 'price']
    list_template_name = 'flights.html'
    detail_template_name = 'flight.html'


class HotelsView(ReadonlyBaseView):
    model = Hotel
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    search_fields = ['name', 'location', 'price_per_night']
    list_template_name = 'hotels.html'
    detail_template_name = 'hotel.html'


class ActivitiesView(ReadonlyBaseView):
    model = Activity
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    search_fields = ['name', 'location', 'price']
    list_template_name = 'activities.html'
    detail_template_name = 'activity.html'


class PackagesView(ReadonlyBaseView):
    model = Package
    serializer_class = PackageGETSerializer
    queryset = Package.objects.all()
    search_fields = [
        'name', 'price', 'hotels__name', 'hotels__price_per_night',
        'flights__airline', 'flights__price', 'activities__name',
        'activities__price'
    ]
    list_template_name = 'packages.html'
    detail_template_name = 'package.html'


class PackageView(BaseView):
    model = Package
    list_template_name = 'packagelist.html'
    detail_template_name = 'packagedetail.html'
    search_fields = [
        'name', 'price', 'hotels__name', 'hotels__price_per_night',
        'flights__airline', 'flights__price', 'activities__name',
        'activities__price'
    ]

    def get_serializer_class(self):
        if self.request.method in ["GET", "OPTIONS"]:
            return PackageGETSerializer
        return PackageCreateSerializer


class Search(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return Response()


class CustomPackageView(HybridViewMixin, viewsets.ModelViewSet):
    detail_template_name = 'my-package.html'
    serializer_class = CustomPackageGet

    def get_queryset(self):
        return CustomPackage.objects.filter(customer=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return CustomPackageGet
        return CustomPackageSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if CustomPackage.objects.filter(customer=user).exists():
            instance = CustomPackage.objects.get(customer=user)
            return Response({'id': instance.id}, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            return super().create(request, *args, **kwargs)

    def render_html(self, request, *args, **kwargs):
        request.query_params = request.GET
        if kwargs.get('pk') is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = queryset
            return render(request, self.list_template_name, context={'items': serializer})
        else:
            serializer = self.get_object()
            return render(request, self.detail_template_name, context={'item': serializer})


class BookingView(HybridViewMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    list_template_name = 'my-bookings.html'
    detail_template_name = 'my-booking.html'

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return mybookingget
        return mybookingser

    def render_html(self, request, *args, **kwargs):
        request.query_params = request.GET
        if kwargs.get('pk') is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = queryset
            return render(request, self.list_template_name, context={'items': serializer})
        else:
            serializer = self.get_object()
            return render(request, self.detail_template_name, context={'item': serializer})


class BookingsView(HybridViewMixin, viewsets.ModelViewSet):
    http_method_names = ['get']
    list_template_name = 'mbookings.html'
    serializer_class = CustomPackageGet

    def get_queryset(self):
        return Booking.objects.filter(
            Q(package__agency__agent=self.request.user)
            | Q(custom__hotels__agency__agent=self.request.user)
            | Q(custom__flights__agency__agent=self.request.user)
            | Q(custom__activities__agency__agent=self.request.user),
            is_paid=True
        )

    def get_serializer_class(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return mybookingget

    def render_html(self, request, *args, **kwargs):
        request.query_params = request.GET
        if kwargs.get('pk') is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = queryset
            return render(request, self.list_template_name, context={'items': serializer})
        else:
            serializer = self.get_object()
            return render(request, self.detail_template_name, context={'item': serializer})


class PaymentView(CreateAPIView):
    serializer_class = PaymentSerializier

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            booking = Booking.objects.get(pk=data.get('booking'))
            id = booking.id
            price = booking.total_cost
            stripe.api_key = 'sk_test_51P4SkgSAO2thxTug2XphjVtTksy9Q9QgaK28Bq9kvsaxJoWGxqKBYUa9Z6zFg9AhTCpQ2y9Cb87yMNpYhK98s1HO00nYORxaOY'
            try:

                price = stripe.Price.create(
                    unit_amount=int(price*100),
                    currency='usd',
                    product_data={"name": "Travell Package"}
                )

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price": price.id,
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url='http://127.0.0.1:8000' + f'/success/{id}/',
                    cancel_url='http://127.0.0.1:8000' + '/cancel/',
                )
                return Response({"url": checkout_session.url}, status=status.HTTP_302_FOUND)
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SuccessView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        booking = Booking.objects.get(pk=id)
        booking.is_paid = True
        booking.save()
        Payment.objects.create(booking=booking, amount=booking.total_cost)
        return render(request, 'success.html')


class SearchView(GenericAPIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)

        if not search_query:
            return Response({'error': 'Search query parameter is missing'}, status=400)
        flights = Flight.objects.filter(
            Q(airline__icontains=search_query) |
            Q(agency__name__icontains=search_query)
        )

        hotels = Hotel.objects.filter(
            Q(name__icontains=search_query) |
            Q(agency__name__icontains=search_query)
        )

        activities = Activity.objects.filter(
            Q(name__icontains=search_query) |
            Q(agency__name__icontains=search_query)
        )

        flight_serializer = FlightSerializer(flights, many=True)
        hotel_serializer = HotelSerializer(hotels, many=True)
        activity_serializer = ActivitySerializer(activities, many=True)

        return Response({
            'flights': flight_serializer.data,
            'hotels': hotel_serializer.data,
            'activities': activity_serializer.data
        })
