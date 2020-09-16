from twilio.rest import Client
from .credentials import account_sid,auth_token,my_cello,my_twilio

client = Client(account_sid,auth_token)


def sms(otp,phonenumber):
    client.messages.create(to=my_cello, from_=my_twilio, body="your verification code is {0}".format(otp))