from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
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
from django.http import HttpResponseRedirect
import requests




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
        if self.request.user.is_authenticated: # Checking if user is authenticated to create carts
            context['has_cart'] = ShoppingCart.objects.filter(user=self.request.user).exists()
        else:
            context['has_cart'] = False
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
        if self.request.user.is_authenticated: # Checking if user is authenticated to create carts
            context['has_cart'] = ShoppingCart.objects.filter(user=self.request.user).exists()
        else:
            context['has_cart'] = False
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
    """
    Handles the display of a list of all airports.
    """
    model = Airport
    template_name = 'flights/airport_list.html' 
    context_object_name = 'airports' 

    def get_context_data(self, **kwargs):
        """
        Adds extra context data to the list view if needed.
        """
        context = super().get_context_data(**kwargs)
        return context


# Detail view for a specific airport
class AirportDetailView(DetailView):
    """
    Handles the display of details for a specific airport.
    """
    model = Airport
    template_name = 'flights/airport_detail.html' 
    context_object_name = 'airport'  

    def get_context_data(self, **kwargs):
        """
        Adds extra context data to the detail view if needed.
        """
        context = super().get_context_data(**kwargs)
        context['departing_flights'] = Flight.objects.filter(departure_airport=self.object)
        context['arriving_fligths'] = Flight.objects.filter(arrival_airport=self.object)
        return context


# Shopping cart creation view
class ShoppingCartCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a shopping cart for the logged-in user.
    """
    model = ShoppingCart
    template_name = 'flights/create_cart.html'  # Optional: Create a specific template if needed
    fields = []  # No fields required, as the user is assigned programmatically

    def form_valid(self, form):
        """
        Automatically assigns the logged-in user to the shopping cart upon creation.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects the user to their shopping cart after it is created.
        """
        return reverse_lazy('shopping_cart')


# Shopping cart view
class ShoppingCartView(LoginRequiredMixin, ListView):
    """
    Handle the display of the shopping cart.
    Displays all flights in the logged-in user's shopping cart, along with the total price.
    """
    model = ShoppingCart
    template_name = 'flights/shopping_cart.html'
    context_object_name = 'shopping_cart'

    def get_context_data(self, **kwargs):
        """
        Retrieves the shopping cart data, including flights and total price, for the logged-in user.
        """
        context = super().get_context_data(**kwargs)
        # Ensure a shopping cart exists for the user
        cart, created = ShoppingCart.objects.get_or_create(user=self.request.user)
        context['cart_flights'] = ShoppingCartFlight.objects.filter(cart=cart)
        context['total_price'] = cart.total_price
        return context

class CheckoutView(LoginRequiredMixin, View):
    """
    Handles the checkout process for the shopping cart.
    Queries the SerpAPI for purchasing options for flights in the shopping cart.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request for the checkout page.
        Retrieves flights in the shopping cart and queries SerpAPI.
        """
        cart = request.user.shopping_cart
        cart_flights = cart.cart_flights.all()
        serpapi_results = []

        for cart_flight in cart_flights:
            # Prepare parameters for SerpAPI
            print(cart_flight.flight.departure_airport.code)
            print(cart_flight.flight.arrival_airport.code)
            print(cart_flight.flight.departure_time.strftime("%Y-%m-%d"))
            airline_code = cart_flight.flight.flight_number[:2]
            params = {
                "engine": "google_flights",
                "departure_id": cart_flight.flight.departure_airport.code,
                "arrival_id": cart_flight.flight.arrival_airport.code,
                "outbound_date": cart_flight.flight.departure_time.strftime("%Y-%m-%d"),
                "currency": "USD",
                "hl": "en",
                "type": "2",
                # "include_airlines": airline_code,
                # "deep_search": "true",
                "api_key": "d764904413d0f85fcb35954a94356a3cb2c27e21726f437941bcdbfdeb166d3d",
            }

            # Make the request to SerpAPI
            try:
                response = requests.get("https://serpapi.com/search.json", params=params)
                if response.status_code == 200:
                    flight_data = response.json()
                    for best_flight in flight_data.get("best_flights", []):
                        best_flight["last_arrival_airport"] = best_flight["flights"][-1]["arrival_airport"]["name"]
                    serpapi_results.append(flight_data)
                else:
                    serpapi_results.append({"error": response.text})  # Log full error
            except requests.RequestException as e:
                serpapi_results.append({"error": str(e)})


        # Render the checkout page with SerpAPI results
        return render(request, "flights/checkout.html", {"serpapi_results": serpapi_results})


# Add flight to shopping cart view
class AddFlightToCartView(LoginRequiredMixin, UpdateView):
    """
    Add a flight to the logged-in user's shopping cart.
    """
    model = ShoppingCartFlight
    fields = []  # No additional input required; handled internally.

    def post(self, request, *args, **kwargs):
        """
        Adds a flight to the user's shopping cart and redirects back to the shopping cart view.
        Ensures the cart exists for the user before adding the flight.
        """
        cart, created = ShoppingCart.objects.get_or_create(user=self.request.user)
        flight = Flight.objects.get(pk=kwargs['pk'])
        ShoppingCartFlight.objects.create(cart=cart, flight=flight)
        return redirect('shopping_cart')


# Delete shopping cart view
class DeleteShoppingCartView(LoginRequiredMixin, DeleteView):
    """
    Delete the entire shopping cart for the logged-in user.
    """
    model = ShoppingCart

    def get_object(self, queryset=None):
        """
        Fetches the shopping cart object belonging to the logged-in user.
        """
        print("DeleteShoppingCartView is being called")
        return ShoppingCart.objects.get(user=self.request.user)
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully deleting the cart.'''
        return reverse('all_flights')

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