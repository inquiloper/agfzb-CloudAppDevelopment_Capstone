from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from django.urls import reverse

from djangoapp.restapis import get_dealers_from_cf
from djangoapp.restapis import get_dealer_reviews_from_cf
from djangoapp.restapis import post_request
from djangoapp.models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

def registration(request):
    return render(request, 'djangoapp/registration.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return redirect(reverse('djangoapp:index'))
    else:
        return redirect(reverse('djangoapp:index'))
    
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request=request)
    return redirect(reverse('djangoapp:index'))

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    password = request.POST['password']
    
    user = User.objects.create_user(username, password=password, first_name=first_name, last_name=last_name)
    user.save()
    return redirect(reverse('djangoapp:index'))

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://c2ee791a.us-south.apigw.appdomain.cloud/api/dealership"
        context['dealerships'] = get_dealers_from_cf(url)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://c2ee791a.us-south.apigw.appdomain.cloud/api/review"
        context['reviews'] = get_dealer_reviews_from_cf(url, dealer_id)
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            car = CarModel.objects.get(pk= request.POST['car'])
            print(request.POST)

            if 'purchasecheck' in request.POST:
                purchased = True
            else:
                purchased = False
                
            review = {}
            review['name'] = user.username
            review['dealership'] = dealer_id
            review['purchase'] = purchased
            review['review'] = request.POST['content']
            review['purchase_date'] = request.POST['purchasedate']
            review['car_model'] = car.name
            review['car_year'] = car.year.strftime('%Y')
            review['car_make'] = car.maker.name
            review['time'] = datetime.now().isoformat()
            
            json_payload = {'review': review}
            
            response = post_request("https://c2ee791a.us-south.apigw.appdomain.cloud/api/review", json_payload=json_payload, dealerId=dealer_id)
            
            return redirect('djangoapp:get_dealer_details', dealer_id=dealer_id)
        else:
            context = {}
            print(request.user)
            context['dealer_id'] = dealer_id
            context['cars'] = CarModel.objects.all()
            dealer = get_dealers_from_cf("https://c2ee791a.us-south.apigw.appdomain.cloud/api/dealership", dealerId=dealer_id)
            context['dealer'] = dealer[0]
            return render(request, 'djangoapp/add_review.html', context)
    
    
    
