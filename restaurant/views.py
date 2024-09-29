from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
from datetime import datetime, timedelta

# Create your views here.

chiptole_image = "https://image.cnbcfm.com/api/v1/image/106304982-15767633092704_chipotle_2019-206.jpg?v=1676813128"

menu = [
    {"name": "Burrito", "price": 15.00, "options": ["Spicy", "White Rice", "Brown Rice", "Corn", "Steak", "Chicken"]},
    {"name": "Bowl", "price": 20.00, "options": ["Cheese", "White Rice", "Black beans", "Steak", "Lettuce"]},
    {"name": "Tacos", "price": 8.99},
    {"name": "Chips", "price": 4.98, "options": ["Guac", "Queso"]}
]

daily_special = [
    {"name": "Salad", "price": 20.00},
    {"name": "Pizza from Otto", "price": 10.00, "options": ["Pepperoni", "Sausage", "Pineapple"]},
    {"name": "Lemonade", "price": 3.99}
]

def main(request):
    '''Show the main page'''

    template_name = 'restaurant/main.html'

    context = {
        "image": chiptole_image,
    }

    '''We are letting the render build a response using that template'''
    return render(request, template_name, context)

def order(request):
    '''Show the form page'''

    template_name = 'restaurant/order.html'

    context = {
        "menu": menu,
        "special": random.choice(daily_special),
    }

    return render(request, template_name, context)

def confirmation(request):
    '''Handle form submission'''

    template_name = 'restaurant/confirmation.html'
    context={}

    # check that we have a POST request
    if request.POST:
        # read the form data into python variables
        customer_name = request.POST['name']
        customer_phone = request.POST['phone']
        customer_email = request.POST['email']
        
        comments = request.POST['comments']

        order_items = request.POST.getlist('items')
        daily_spec = request.POST.get('daily_special')

        total_price = 0
        options = {}

        # Loop through selected items and calculate total price
        for item in order_items:
            # Check if the item exists in the main menu or daily specials and get its price
            for menu_item in menu + daily_special:
                if menu_item['name'] == item:
                    total_price += menu_item['price']

                    # item_options = request.POST.getlist(f'options_{menu_item["name"]}')
                    # options[menu_item['name']] = item_options

        if daily_spec:
            for special in daily_special:
                if special['name'] == daily_spec:
                    total_price += special['price']

                    # item_options = request.POST.getlist(f'options_{special["name"]}')
                    # options[special['name']] = item_options



        random_min = random.randint(15,30)
        ready_time = datetime.now() + timedelta(minutes=random_min)

        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'comments': comments,
            'price': total_price,
            'ordered_items': order_items,
            'ready_time': ready_time,
            'special': daily_spec,
            'options': options,
        }
        return render(request, template_name, context) 




    return redirect("main")