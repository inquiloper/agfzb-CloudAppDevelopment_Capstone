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
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)
        # return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://c2ee791a.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        return HttpResponse(reviews)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    # TODO: check if user is authenticated
    review = {}
    review.name = request.POST['name']
    review.dealership = dealer_id
    review.purchase= request.POST['purchase']
    review.review = request.POST['review']
    review.purchase_date = request.POST['purchase_date']
    review.car_make = request.POST['car_make']
    review.car_model = request.POST['car_model']
    review.car_year =  request.POST['car_year']
    review.time = datetime.now().isoformat()
    
    json_payload = {'review': review}
    
    response = post_request("https://c2ee791a.us-south.apigw.appdomain.cloud/api/review", json_payload=json_payload, dealerId=dealer_id)
    
    return HttpResponse(response)
    
    
