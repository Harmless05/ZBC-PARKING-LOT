from user import User
from card import Card
from invoice import Invoice
from car import Car
from sensor import Sensor


class Manager:
    parking_spots = []

    def get_or_create_car(self, license_plate):
        pass

    def register_card(self, card_number, cvv, exp_year, exp_month):
        pass

    def register_invoice(self, start_date, end_date, license_plate, parking_price):
        pass
