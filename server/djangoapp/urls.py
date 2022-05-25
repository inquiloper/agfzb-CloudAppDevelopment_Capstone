from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path(route='registration', view=views.registration, name='registration'),
    
    # path for registration request
    path(route='registration_request', view=views.registration_request, name="registration_request"),

    # path for login
    path(route='login', view=views.login_request, name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='get_dealer_details'),

    # path for add a review view
    path(route='dealer/<int:dealer_id>/review', view=views.add_review, name='add_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)