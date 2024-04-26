from rest_framework import serializers
from .models import Agency, Flight, Hotel, Activity, Package, CustomPackage, Booking, Payment


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'
        read_only_fields = ['agent']

    def create(self, validated_data):
        validated_data['agent'] = self.context.get('request').user
        return super().create(validated_data)


class Baseserializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context.get('request').user
        agency = Agency.objects.get(agent=user)
        validated_data['agency'] = agency
        return super().create(validated_data)


class ImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())
    flight = serializers.CharField(allow_null=True, required=False)
    hotel = serializers.CharField(allow_null=True, required=False)
    activity = serializers.CharField(allow_null=True, required=False)


class FlightSerializer(Baseserializer):
    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ['agency']
        depth = 1


class HotelSerializer(Baseserializer):
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['agency']
        depth = 1


class ActivitySerializer(Baseserializer):
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['agency']
        depth = 1


class PackageGETSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = '__all__'
        depth = 1


class PackageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ['agency', 'price']

    def create(self, validated_data):
        hotels = validated_data.get('hotels')
        flights = validated_data.get('flights')
        activities = validated_data.get('activities')

        hotel_prices = 0
        flight_prices = 0
        ac_prices = 0
        if hotels:
            for hotel in hotels:
                hotel_prices += hotel.price_per_night
        if flights:
            for flight in flights:
                flight_prices += flight.price
        if activities:
            for acc in activities:
                ac_prices += acc.price
        user = self.context.get('request').user
        agency = Agency.objects.get(agent=user)
        validated_data['agency'] = agency
        validated_data['price'] = hotel_prices + flight_prices + ac_prices
        return super().create(validated_data)

    def update(self, instance, validated_data):
        hotels = validated_data.get('hotels')
        flights = validated_data.get('flights')
        activities = validated_data.get('activities')

        hotel_prices = 0
        flight_prices = 0
        ac_prices = 0
        if hotels:
            for hotel in hotels:
                hotel_prices += hotel.price_per_night
        if flights:
            for flight in flights:
                flight_prices += flight.price
        if activities:
            for acc in activities:
                ac_prices += acc.price
        validated_data['price'] = hotel_prices + flight_prices + ac_prices
        return super().update(instance, validated_data)


class CustomPackageGet(serializers.ModelSerializer):
    class Meta:
        model = CustomPackage
        exclude = ['customer']
        read_only_fields = ['price']
        depth = 1


class CustomPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPackage
        exclude = ['customer']
        read_only_fields = ['price']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['customer'] = user
        hotels = validated_data.get('hotels')
        flights = validated_data.get('flights')
        activities = validated_data.get('activities')

        hotel_prices = 0
        flight_prices = 0
        ac_prices = 0
        if hotels:
            for hotel in hotels:
                hotel_prices += hotel.price_per_night
        if flights:
            for flight in flights:
                flight_prices += flight.price
        if activities:
            for acc in activities:
                ac_prices += acc.price
        validated_data['price'] = hotel_prices + flight_prices + ac_prices
        return super().create(validated_data)

    def update(self, instance, validated_data):
        hotels = validated_data.get('hotels')
        flights = validated_data.get('flights')
        activities = validated_data.get('activities')
        hotel_prices = flight_prices = ac_prices = 0
        if self.context.get('request').method == 'PATCH':
            hotel_prices = sum(hotel.price_per_night for hotel in instance.hotels.all(
            )) if instance.hotels.all() else 0
            flight_prices = sum(flight.price for flight in instance.flights.all(
            )) if instance.flights.all() else 0
            ac_prices = sum(activity.price for activity in instance.activities.all(
            )) if instance.activities.all() else 0
        if hotels:
            for hotel in hotels:
                if hotel.id not in instance.hotels.all().values_list('id', flat=True) or self.context.get('request').method != 'PATCH':
                    hotel_prices += hotel.price_per_night
        if flights:
            for flight in flights:
                if flight.id not in instance.flights.all().values_list('id', flat=True) or self.context.get('request').method != 'PATCH':
                    flight_prices += flight.price
        if activities:
            for acc in activities:
                if acc.id not in instance.activities.all().values_list('id', flat=True) or self.context.get('request').method != 'PATCH':
                    ac_prices += acc.price
        validated_data['price'] = hotel_prices + flight_prices + ac_prices
        return super().update(instance, validated_data)


class mybookingget(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        depth = 2


class mybookingser(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['customer', 'payment_info', 'total_cost', 'is_paid']

    def create(self, validated_data):
        if validated_data.get('package'):
            validated_data['total_cost'] = validated_data.get('package').price
        elif validated_data.get('custom'):
            validated_data['total_cost'] = validated_data.get('custom').price
        validated_data['customer'] = self.context.get('request').user
        return super().create(validated_data)


class PaymentSerializier(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking']

    def create(self, validated_data):
        validated_data['amount'] = validated_data.get('booking').total_cost
        validated_data.get('booking').is_paid = True
        validated_data.get('booking').save()
        return super().create(validated_data)
