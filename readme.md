## **TicketVendor**

This Rest api will manages all the tickets for the shows, movies and concerts. This API is built on the top of the django rest framework.

<img src="Ticket Vendor.png">

#### Note : -
There is not mention of add seat in a database. So i had implemented another endpoint. So refer the 4 endpoint list below. First add a single Seat then proceed with other endpoint.

#### Steps to run the django app:-

1. Create a virtual env with `python3 -m venv env`
2. Activate virtual env with `. env/bin/activate`
3. Install requirements using `pip install -r requirements.txt`
4. Run the server locally using `python3 manage.py runserver`
5. Go to `http://127.0.0.1:8000/`

#### **Endpoints**
1. /api/vacate : This endpoint takes the person name and the seat number to vacate that particular seat. Make a post request to this endpoint with content type="application/json"
<br> Example :-
<br> Endpoint `http://127.0.0.1:8000/api/vacate/ `
<br> Data
`{
 "SEATNUM":"A1"
}`

2. /api/get_info/[ticket_id or Person name or Seat no] : This endpoint will provide you all the information about your ticket.
Simple add the ticket_id or Person name or Seat no in the url and it will give a response in json format.
<br> Example : - Direct url `http://127.0.0.1:8000/api/get_info/A1`

3. api/occupy : This endpoint will search all the seat. If it finds one then it will book  that for you and provide details in response but if it unable to find one then it will raise 404 status code with All seats reserved.
<br> Example : -
<br> Endpoint  `http://127.0.0.1:8000/api/occupy`
<br> Data `{
        "ticket_id": "2edc7cc5-f436-4104-b799-64ca94cd3e2e",
        "person_name": "Praveen Chaudhary"
}`

4. /api/add_seat : This endpoint will add seat to the database and checks that the number of seat will not exceed the MAX_OCCUPANCY 
<br> Example : -
<br> Endpoint `http://127.0.0.1:8000/api/add_seat`
<br> Data `{
    "SEATNUM": "A2"
}`

### Topics -> python, django, django-rest-framework, webdevelopment, api  

<h5>Source Code Link -> <u><a href="https://github.com/chaudharypraveen98/TicketVendor">GitHub</a></u></h5>

### What We are going to do?  
<ol>
    <li>Starting the TicketVendor django Project</li>
    <li>Creating a booking app within the TicketVendor Project</li>
    <li>Create a Order and Seat in booking/models.py</li>
    <li>Writing serializers for booking model data</li>
    <li>Creating a view for handling the request made from the client</li>
    <li>Adding function handlers to routes</li>
</ol>  

### Understanding Some Important Concepts  

### What is Django Framework?  

Django is a Python-based free and open-source web framework that follows the model–template–views architectural pattern.

**Top Features of Django Framework**  

<ul>
    <li>Excellent Documentation</li>
    <li>SEO Optimized</li>
    <li>High Scalability</li>
    <li>Versatile in Nature</li>
    <li>Offers High Security</li>
    <li>Provides Rapid Development</li>
</ul>

### Django REST framework ?  

Django REST framework is a powerful and flexible toolkit for building Web APIs.
Some reasons you might want to use REST framework:

<ul>
    <li>The <a href="https://restframework.herokuapp.com/">Web browsable API</a> is a huge usability win for your developers.</li>
    <li><a href="api-guide/authentication/">Authentication policies</a> including packages for <a href="api-guide/authentication/#django-rest-framework-oauth">OAuth1a</a> and <a href="api-guide/authentication/#django-oauth-toolkit">OAuth2</a>.</li>
    <li><a href="api-guide/serializers/">Serialization</a> that supports both <a href="api-guide/serializers#modelserializer">ORM</a> and <a href="api-guide/serializers#serializers">non-ORM</a> data sources.</li>
    <li>Customizable all the way down - just use <a href="api-guide/views#function-based-views">regular function-based views</a> if you don't need the <a href="api-guide/generic-views/">more</a> <a href="api-guide/viewsets/">powerful</a> <a href="api-guide/routers/">features</a>.</li>
    <li>Extensive documentation, and <a href="https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework">great community support</a>.</li>
    <li>Used and trusted by internationally recognised booking including <a href="https://www.mozilla.org/en-US/about/">Mozilla</a>, <a href="https://www.redhat.com/">Red Hat</a>, <a href="https://www.heroku.com/">Heroku</a>, and <a href="https://www.eventbrite.co.uk/about/">Eventbrite</a>.</li>
</ul>


## Step 1 => Starting the Django Project

Initialize a Django project by following command. **Python** must be installed on your system.

```
pip install Django
pip install djangorestframework
```

You can confirm the installation by checking the django version by following command

```
python -m django --version
```


**Starting the Project**

```
django-admin startproject TicketVendor
```


You get the project structure like this

```
TicketVendor/
    manage.py
    TicketVendor/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```


## Step 2 -> Creating a booking app within the TicketVendor Project  

### What is a Django App?  

An app is a Web application that does something – e.g., a Weblog system, a database of public records or a small poll app. 

A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

Creating the booking app

```
python manage.py startapp booking
```

That’ll create a directory booking, which is laid out like this:

```
booking/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

### Including your app and libraries in project

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # framework for making rest api
    'rest_framework',

    # our main reusable components
    'booking.apps.BookingConfig'
]
```


## Step 3 -> Create a Order and Seat model in booking/models.py  

### What is a Django Model?  

A model is the single, definitive source of truth about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. 

The goal is to define your data model in one place and automatically derive things from it.

Let's create a Django Model
.
A database contains a number of variable which are represented by fields in django model.Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

```
import uuid

from django.db import models


class Seat(models.Model):
    SEATNUM = models.CharField(max_length=8)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.SEATNUM} {str(self.status)}"


class Orders(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='ticket_orders', null=True, blank=True)
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    person_name = models.CharField(max_length=30)

    def __str__(self):
        return self.person_name
```

Here, Two concepts are used
<ol>
    <li>Primary Key</li>
    <li>Foreign Key</li>
</ol>

A **primary key** is used to ensure data in the specific column is unique. A **foreign key** is a column or group of columns in a relational database table that provides a link between data in two tables. 

Here, We have used the one to many relationship between the Orders and Seats as there can be many orders for Seat.

### Adding models to admin panel  

Django provides built-in admin panel to manage the data into model  

```
from django.contrib import admin

# Register your models here.
from booking.models import Seat, Orders

admin.site.register(Seat)
admin.site.register(Orders)
```

### Making migrations  

Once the model is defined, the django will automatically take schemas and table according to the fields supplied in the django model.

```
python manage.py makemigrations
python manage.py migrate
```



## Step 4 -> Writing serializers for booking model data  

### What are Serializers?  

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. 

Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.


### We are using Model Serializer. But Why?  

The <tt>ModelSerializer</tt> class provides a shortcut that lets you automatically create a <tt>Serializer</tt> class with fields that correspond to the Model fields.


### The <tt>ModelSerializer</tt> class is the same as a regular <tt>Serializer</tt> class, except that:

<ul>
    <li>It will automatically generate a set of fields for you, based on the model.</li>
    <li>It will automatically generate validators for the serializer, such as unique_together validators.</li>
</ul>

```
from rest_framework import serializers

from booking.models import Orders, Seat


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

```

Here we are using **ModelSerializer** for Order and Seat model


## Step 5 -> Creating a view for handling the request made from the client.  

### What is a Django View?  

A view function, or view for short, is a Python function that takes a Web request and returns a Web response. 

### Http Methods  

<table>
    <thead>
        <tr>
            <th>HTTP Verb</th>
            <th>CRUD</th>
            <th>Entire Collection (e.g. /customers)</th>
            <th>Specific Item (e.g. /customers/{id})</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>POST</td>
            <td>Create</td>
            <td>201 (Created), 'Location' header with link to /customers/{id} containing new ID.</td>
            <td>404 (Not Found), 409 (Conflict) if resource already exists..</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>Read</td>
            <td>200 (OK), list of customers. Use pagination, sorting and filtering to navigate big lists.</td>
            <td>200 (OK), single customer. 404 (Not Found), if ID not found or invalid.</td>
        </tr>
        <tr>
            <td>PUT</td>
            <td>Update/Replace</td>
            <td>405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection.</td>
            <td>200 (OK) or 204 (No Content).  404 (Not Found), if ID not found or invalid.</td>
        </tr>
        <tr>
            <td>PATCH</td>
            <td>Update/Modify</td>
            <td>405 (Method Not Allowed), unless you want to modify the collection itself.</td>
            <td>200 (OK) or 204 (No Content).  404 (Not Found), if ID not found or invalid.</td>
        </tr>
        <tr>
            <td>DELETE</td>
            <td>Delete</td>
            <td>405 (Method Not Allowed), unless you want to delete the whole collection—not often desirable.</td>
            <td>200 (OK).  404 (Not Found), if ID not found or invalid.</td>
        </tr>
    </tbody>
</table>


### booking/views.py  

**Importing libraries, models and serializers**  

```
from uuid import UUID

from django.db.models import Q
from rest_framework import status, exceptions
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from TicketVendor.settings import MAX_OCCUPANCY
from booking.models import Orders, Seat
from booking.serializers import OrderSerializer, SeatSerializer
```

**Vacating the Seat if occupied**  

```
class VacateApi(APIView):
    """
    This class will update the status of seats
    """

    def post(self, request, *args, **kwargs):
        seat_objects = Seat.objects.filter(SEATNUM=request.data['SEATNUM'])
        if seat_objects.exists() and seat_objects[0].status is True:
            seat = Seat.objects.get(pk=seat_objects[0].pk)
            seat.status = False
            seat.save()
            return Response("updated status", status=status.HTTP_200_OK)
        return Response("Seat not Found or Already vacant", status=status.HTTP_404_NOT_FOUND)
```

**Booking / Occupying seat**  

```
class OccupyApi(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()

    def get(self, request, **kwargs):
        return self.list(request)

    def perform_create(self, serializer):
        # It will check the free seats
        all_seats = Seat.objects.filter(status=False)
        if all_seats.exists():
            seat = Seat.objects.get(pk=all_seats[0].pk)
            seat.status = True
            seat.save()
        else:
            # if free slot not present raise exception
            raise NotFound(detail="All seats Resereved", code=404)
        serializer.save(seat=seat)

    def post(self, request, **kwargs):
        return self.create(request)
```

**Getting ticket info**  

```
class GetInfoApi(GenericAPIView):

    def validate_uuid4(self, uuid_string):
        # This function checks the valid UUID
        try:
            val = UUID(uuid_string, version=4)
        except ValueError:
            return False

        return True

    def get_object(self, **kwargs):
        # Here key refers to the request data , it can be ticket id , person name or seat number
        key = kwargs['key']

        # First it tries to find the ticket using seat no and person name
        ticket = Orders.objects.filter(Q(seat__SEATNUM=key) | Q(person_name=key))
        if ticket.exists():
            return ticket[0]

        # It check if uuid is valid or not
        valid_uuid = self.validate_uuid4(key)
        if valid_uuid:
            ticket = Orders.objects.filter(ticket_id=key)
            if ticket.exists:
                return ticket[0]
        raise exceptions.NotFound(detail="No Result Found", code=404)

    def get(self, request, *args, **kwargs):
        ticket = self.get_object(**kwargs)
        serializer = OrderSerializer(instance=ticket)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Adding seat to Hall**  

```
class AddSeatApi(CreateModelMixin):
    serializer_class = SeatSerializer

    # this function will overwrite the default create Model mixin, We can even use the APIview class too.
    def create(self, request, *args, **kwargs):
        total_seat = Seat.objects.count()
        if total_seat > MAX_OCCUPANCY-1:
            return Response("Seat exceeds the MAX_OCCUPANCY", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

We are using Django <tt>Response</tt> in-built function.

Arguments:
<ul>
    <li><tt>data</tt>: The serialized data for the response.</li>
    <li><tt>status</tt>: A status code for the response.  Defaults to 200.  See also <a href="../status-codes/">status codes</a>.</li>
    <li><tt>template_name</tt>: A template name to use if <tt>HTMLRenderer</tt> is selected.</li>
    <li><tt>headers</tt>: A dictionary of HTTP headers to use in the response.</li>
    <li><tt>content_type</tt>: The content type of the response.  Typically, this will be set automatically by the renderer as determined by content negotiation, but there may be some cases where you need to specify the content type explicitly.</li>
</ul>



## Step 6 -> Adding function handlers to routes.(booking/urls.py)  

Whenever user visit the user, a function is called in view which takes care of response.

**TicketVendor/urls.py**

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('booking.urls'))
]
```

**Adding sub path for booking app(booking/urls.py)**  

It defines the particular path for booking app  

```
from django.urls import path

from booking import views

urlpatterns = [
    path('vacate/', views.VacateApi.as_view()),
    path('occupy/', views.OccupyApi.as_view()),
    path('get_info/<str:key>', views.GetInfoApi.as_view()),
    path('add_seat', views.AddSeatApi.as_view())
]
```

#### Note  
Feel free to make changes and give suggestions. All pull request are most welcomed

