import random
from locust import HttpUser, TaskSet, between, constant
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
    # l.client.get("/product/" + product)
    l.client.post("/cart", {
        'product_id': product,
        'quantity': random.choice([1,2,3,4,5,10])})

def checkout(l):
    # addToCart(l)
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
