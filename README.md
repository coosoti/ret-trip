# RetTrip

## Introduction

RetTrip is a mobile friendly app built with Django framework. It is a platform that allows drivers of public service vehicles and truckers with vacant spaces to pick and drop off parcels along their way as they make return trips. The customers can in real-time access the location of their packages on transit. 

Ordinarily, this app needs to be built in either native android or native ios languages but for now it is built for the web.

## Technologies

**Front-end**

* HTML, CSS & JavaScript
* Bootstrap 4.6
* jQuery library
* bootoast
* awesome front

**Backend**

* Python 3.8
* Django 3
* SQLite

**APIS**

* Google Maps Places API
* Google Maps direction matrix API
* Stripe Payment Gateway API
* Firebase

## Installation

__Note__: 

* Clone my repository

`$ git clone https://github.com/coosoti/ret-trip.git`

* cd into ret-trip

`$ cd ret-trip`

* Create a virtual environment

`$ python3 -m venv env`

* Activate virtual environment

`$ source env/bin/activate`

* Install dependecies

`(env) $ pip install -r requirements.txt`

* run the server

`(env) $ python manage.py runserver`

    **__Note__**

    For this app to run in your localhost, you need a set up a few api keys including:
        - facebook authentication api
        - google maps places api
        - google maps direction matrix api
        - stripe payment gateway api
        - firebase api

## usage

* Visit the link http://127.0.0.1:8000 on your local machine to interact with the app

- You can register two users; a driver and a customer
- Use two different browsers for each category of user
- the customer can post tasks in the form of packages they want delivered
- the driver may then see the tasks and either accept or ignore them
- if the driver accepts the task, they take picture evidence during pickup
- the customer then starts tracking their package on transit in real time
- the driver drops off the package and a text message is sent to the customer(this feature is in development)

## Contributing

 - Charles Osoti
        [Github](https://github.com/coosoti)

## Related Projects
    - Uber Cargo

## Licensing

MIT License

