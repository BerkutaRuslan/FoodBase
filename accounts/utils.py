import random
from datetime import datetime

from twilio.rest import Client

from FoodBase import settings


def send_sms_code(user_phone):
    """
    Generate 4-digit passcode and send it to user
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    code = str(random.randint(0, 9999)).rjust(4, '0')

    try:
        message = client.messages.create(
            to=str(user_phone),
            from_=settings.TWILIO_NUMBER,
            body=f"Your FoodBase verification code is: {code}"
        )
    except Exception as e:
        print(e)
        return None
    else:
        return code


def update_review_date(employee):
    employee.review_date = datetime.today().date()
    employee.save()
    return employee
