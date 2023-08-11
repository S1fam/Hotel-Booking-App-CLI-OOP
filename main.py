import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:

    def __init__(self, hotels_id):
        self.hotel_id = hotels_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        pass

    def view(self):
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


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class SpaTicket(SpaHotel):
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
                Thank you for your SPA reservation!
                Here are your SPA booking data:
                Name: {self.customer_name}
                Hotel: {self.hotel.name}
                """
        return content


class ReservationTicket:

    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:  # if passed dict in df dict
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        card_password = df_cards_security.loc[df_cards_security["number"] == self.number,
                                              "password"].squeeze()
        if card_password == given_password:
            return True
        else:
            return False


print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234")  # we would get the inputed
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        password = input("Card password: ")
        if credit_card.authenticate(given_password=password):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            spa = input("Do you want to book a spa package? [yes/no]: ")
            if spa == "yes":
                hotel.book_spa_package()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())
            else:
                print("okay :C")
                pass
        else:
            print("Credit card authentication failed")
    else:
        print("There was a problem with your payment")
        exit()
else:
    print("Hotel is not free.")
