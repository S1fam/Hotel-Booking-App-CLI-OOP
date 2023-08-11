import pandas
from abc import ABC, abstractmethod

df = pandas.read_csv("hotels.csv", dtype={"id": str})


class Hotel:
    watermark = "The real estate company"

    def __init__(self, hotels_id):
        self.hotel_id = hotels_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        pass

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)
        pass

    def available(self):
        # checks place of df id with inputed id, when finds, checks if df available is yes
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    @classmethod
    def get_hotel_count(cls, data):
        return len(data)

    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False


class Ticket(ABC):

    @abstractmethod
    def generate(self):
        pass


class DigitalTicket(Ticket):
    def generate(self):
        return "Hello, this is your digital ticket"

    def download(self):
        pass


class ReservationTicket(Ticket):

    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.the_customer_name}
        Hotel: {self.hotel.name}
        """
        return content

    @property
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title()
        return name

    @staticmethod
    def convert(amount):
        return amount * 1.2


hotel1 = Hotel(hotels_id="188")
hotel2 = Hotel(hotels_id="134")
hotel3 = Hotel(hotels_id="655")

print(hotel1.name)
print(hotel2.name)

print(hotel1.watermark)
print(hotel2.watermark)

print(Hotel.watermark)

print(Hotel.get_hotel_count(data=df))
print(hotel1.get_hotel_count(data=df))

ticket = ReservationTicket(customer_name="john smith ", hotel_object=hotel1)
print(ticket.the_customer_name)
print(ticket.generate())

converted = ReservationTicket.convert(10)
print(converted)
