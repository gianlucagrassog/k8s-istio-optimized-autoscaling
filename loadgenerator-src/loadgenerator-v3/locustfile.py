#!/usr/bin/python

# █░░ █▀█ ▄▀█ █▀▄   █▀▀ █▀▀ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ █▀█ █▀█  
# █▄▄ █▄█ █▀█ █▄▀   █▄█ ██▄ █░▀█ ██▄ █▀▄ █▀█ ░█░ █▄█ █▀▄  

# █▀▀ █░█ █▀ ▀█▀ █▀█ █▀▄▀█   █▀ █░█ ▄▀█ █▀█ █▀▀
# █▄▄ █▄█ ▄█ ░█░ █▄█ █░▀░█   ▄█ █▀█ █▀█ █▀▀ ██▄

import math
import random
from locust import HttpUser, LoadTestShape, TaskSet
import numpy as np

products = [
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z']

def index(l):
    l.client.get("/")

def setCurrency(l):
    currencies = ['EUR', 'USD', 'JPY', 'CAD']
    l.client.post("/setCurrency",
        {'currency_code': random.choice(currencies)})

def browseProduct(l):
    l.client.get("/product/" + random.choice(products))

def viewCart(l):
    l.client.get("/cart")

def addToCart(l):
    product = random.choice(products)
    #l.client.get("/product/" + product)
    l.client.post("/cart", {
        'product_id': product,
        'quantity': random.choice([1,2,3,4,5,10])})

def checkout(l):
    #addToCart(l)
    l.client.post("/cart/checkout", {
        'email': 'someone@example.com',
        'street_address': '1600 Amphitheatre Parkway',
        'zip_code': '94043',
        'city': 'Mountain View',
        'state': 'CA',
        'country': 'United States',
        'credit_card_number': '4432-8015-6152-0454',
        'credit_card_expiration_month': '1',
        'credit_card_expiration_year': '2039',
        'credit_card_cvv': '672',
    })

class UserBehavior(TaskSet):

    def on_start(self):
        index(self)

    tasks = {index: 1,
        setCurrency: 2,
        browseProduct: 10,
        addToCart: 3,
        viewCart: 3,
        checkout: 1}

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = lambda instance: np.random.exponential(scale=5)  

class DoublePeak(LoadTestShape):
 
    # first stage
    stage = {"duration": 100, "users": 2000, "spawn_rate": 20}

    min_users = 2000 # minimum users
    peak_one_users = 6000 # users in first peak
    peak_two_users = 5500 # users in second peak
    # time_limit = 1200 # total length of test
    time_limit = 1500 # total length of test

    # Normal distribution
    std = 1


    def tick(self):
        run_time = round(self.get_run_time())
        # Reach 200 Users
        if run_time < self.stage["duration"]:
            tick_data = (self.stage["users"], self.stage["spawn_rate"])
            return tick_data
        
        # Start Bell Curve Testing
        else:
            if run_time < self.time_limit:
                user_count = (
                    (self.min_users)
                    + (1/(math.sqrt(2*math.pi)*self.std))
                    * math.e ** ((-1/2)
                                 *(((run_time-8000)/1000)
                                   /
                                   (self.std))**2)
                    * 10000
                )
                # user_count = (
                #     (self.peak_one_users - self.min_users)
                #     * math.e ** -((((run_time + 130 )/ (self.time_limit / 10 * 3.2 / 3)) - 5) ** 2)
                #     + (self.peak_two_users - self.min_users)
                #     * math.e ** -((((run_time + 130)/ (self.time_limit / 10 * 3.2 / 3)) - 10) ** 2)
                #     + self.min_users
                # )
                return (round(user_count), round(user_count))
            else:
                return None
#
