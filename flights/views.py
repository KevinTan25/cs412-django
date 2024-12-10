from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Flight, Airport, AirplaneRental, ShoppingCart, ShoppingCartFlight, ShoppingCartRental
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse as HttpResponse
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login
from typing import Any
from django.urls import reverse



# List view for flights
class FlightListView(ListView):
    '''View all the flights'''
    model = Flight
    template_name = 'flights/show_all_flights.html'
    context_object_name = 'flights'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Text search
        departure_airport = self.request.GET.get('departure_airport')  # Selected departure airport
        arrival_airport = self.request.GET.get('arrival_airport')  # Selected arrival airport

        if query:
            queryset = queryset.filter(
                Q(flight_number__icontains=query)  # Search by flight number
            )
        if departure_airport and departure_airport != "all":
            queryset = queryset.filter(departure_airport__id=departure_airport)
        if arrival_airport and arrival_airport != "all":
            queryset = queryset.filter(arrival_airport__id=arrival_airport)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')  # Pass search term to template
        context['selected_departure_airport'] = self.request.GET.get('departure_airport', 'all')  # Selected departure airport
        context['selected_arrival_airport'] = self.request.GET.get('arrival_airport', 'all')  # Selected arrival airport
        context['airports'] = Airport.objects.all()  # Pass all airports to template
        context['user'] = self.request.user # Return a user
        return context

# Detail view for a specific flight
class FlightDetailView(DetailView):
    '''Handle the specific flight views'''
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the related Airport objects to the context
        context['departure_airport'] = self.object.departure_airport
        context['arrival_airport'] = self.object.arrival_airport
        return context


# Create view for adding a flight
class FlightCreateView(LoginRequiredMixin, CreateView):
    model = Flight
    template_name = 'flights/flight_form.html'
    fields = ['flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'cost', 'aircraft', 'amenities', 'seats_left']
    success_url = reverse_lazy('flights:flight-list')


# Update view for editing a flight
class FlightUpdateView(LoginRequiredMixin, UpdateView):
    model = Flight
    template_name = 'flights/flight_form.html'
    fields = ['flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'cost', 'aircraft', 'amenities', 'seats_left']
    success_url = reverse_lazy('flights:flight-list')


# Delete view for removing a flight
class FlightDeleteView(LoginRequiredMixin, DeleteView):
    model = Flight
    template_name = 'flights/flight_confirm_delete.html'
    success_url = reverse_lazy('flights:flight-list')


# List view for airports
class AirportListView(ListView):
    model = Airport
    template_name = 'flights/airport_list.html'
    context_object_name = 'airports'


# Detail view for a specific airport
class AirportDetailView(DetailView):
    model = Airport
    template_name = 'flights/airport_detail.html'
    context_object_name = 'airport'


# Shopping cart view
class ShoppingCartView(LoginRequiredMixin, ListView):
    '''Handle the display of the shopping cart'''
    model = ShoppingCart
    template_name = 'flights/shopping_cart.html'
    context_object_name = 'shopping_cart'

    def get_queryset(self):
        # Get the logged-in user's shopping cart
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = ShoppingCart.objects.get(user=self.request.user)
        context['cart_flights'] = ShoppingCartFlight.objects.filter(cart=cart)
        context['cart_rentals'] = ShoppingCartRental.objects.filter(cart=cart)
        context['total_price'] = cart.total_price()
        return context

class RegistrationView(CreateView):
    '''Handle registration of new Users.'''

    template_name = 'flights/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''Handle the User creation form submission'''

        if self.request.POST:
            print(f"ReigstrationView.dispatch: self.request.POST={self.request.POST}")

            # reconstruct the UserCreateForm from the POST data
            form = UserCreationForm(self.request.POST)
            
            # if the form isn't value e.c. passwords don't match
            if not form.is_valid():
                print(f"form.errors={form.errors}")
                
                # let CreateView.dispatch handle the problem
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save() # this will commit the insert to the database
            print(f"RegistrationView.dispatch: created user {user}")

            # log the user in
            login(self.request, user)
            print(f"RegistrationView.dispatch: {user} is logged in")
            

            # return a response
            return redirect(reverse('all_flights'))

        # let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)