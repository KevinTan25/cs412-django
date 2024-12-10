from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import timedelta

# Airport model
class Airport(models.Model):
    name = models.CharField(max_length=100)  # Name of the airport
    code = models.CharField(max_length=10, unique=True)  # IATA or ICAO code
    city = models.CharField(max_length=100)  # City where the airport is located
    country = models.CharField(max_length=100)  # Country where the airport is located
    amenities = models.TextField(blank=True, null=True)  # List of amenities available
    avg_security_time = models.DurationField(default=timedelta(minutes=30))  # Default to 30 mins
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

# Aircraft type model
class AircraftType(models.Model):
    model = models.CharField(max_length=50)  # Specific model name
    seat_capacity = models.PositiveIntegerField()  # Total number of seats

    def __str__(self):
        return f"{self.model}"

# Flights model
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)  # Unique flight number
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departing_flights')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arriving_flights')
    departure_time = models.DateTimeField()  # Scheduled departure time
    arrival_time = models.DateTimeField()  # Scheduled arrival time
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of the flight
    aircraft = models.ForeignKey(AircraftType, on_delete=models.CASCADE)  # Aircraft used
    amenities = models.TextField(blank=True, null=True)  # Specific amenities for this flight
    seats_left = models.PositiveIntegerField()  # Number of seats left to book

    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport.code} to {self.arrival_airport.code}"

    @property
    def flight_duration(self):
        return self.arrival_time - self.departure_time

# Airplane Rentals model
class AirplaneRental(models.Model):
    aircraft = models.ForeignKey(AircraftType, on_delete=models.CASCADE)  # Aircraft for rental
    rental_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Rental cost
    amenities = models.TextField(blank=True, null=True)  # Specific amenities for this rental
    available = models.BooleanField(default=True)  # Whether the airplane is available for rental

    def __str__(self):
        return f"{self.aircraft} - Rental"

# Shopping Cart model
class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="shopping_cart"
    )  # Link each shopping cart to one user

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"

    @property
    def total_price(self):
        flights_total = self.cart_flights.filter(cart=self).aggregate(total=Sum('flight__cost'))['total'] or 0
        # rentals_total = sum(
        #     rental.rental.rental_cost * rental.rental_days for rental in self.cart_rentals.all()
        # )
        return flights_total

# Relationship between ShoppingCart and Flight
class ShoppingCartFlight(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_flights')  # Cart reference
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Flight reference
    quantity = models.PositiveIntegerField(default=1)  # Optional, e.g., if one user books multiple tickets

    def __str__(self):
        return f"{self.cart.user.username}'s Cart - Flight {self.flight.flight_number}"

# Relationship between ShoppingCart and AirplaneRental
class ShoppingCartRental(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_rentals')  # Cart reference
    rental = models.ForeignKey(AirplaneRental, on_delete=models.CASCADE)  # Rental reference
    rental_days = models.PositiveIntegerField(default=1)  # Number of days for rental

    def __str__(self):
        return f"{self.cart.user.username}'s Cart - Rental {self.rental.aircraft}"

# Profile model for additional user preferences
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="flights_profile")
    preferences = models.TextField(blank=True, null=True)  # Preferences for filtering flights or rentals

    def __str__(self):
        return f"{self.user.username}'s Profile"
