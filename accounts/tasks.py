from datetime import datetime, timedelta
from celery import shared_task
from FoodBase import settings
from FoodBase.utils import send_email
from accounts.models import Employee
from accounts.utils import update_review_date
from restaurant.models import Restaurant


@shared_task
def employee_salary_review():
    all_restaurants = Restaurant.objects.all()
    for restaurant in all_restaurants:
        review_date = datetime.today() - timedelta(days=restaurant.days_to_review_employee_salary)
        employees_to_review = Employee.objects.filter(restaurant=restaurant.id, review_date__lte=review_date.date())
        if employees_to_review:
            for contact_email in restaurant.email:
                send_email(subject="Review employee salary", user=contact_email, template='salary-review.html',
                           from_email=settings.EMAIL_FROM_SENDER,
                           content={'employee_emails':
                                    f'{[employee.user.email for employee in employees_to_review]}'})
                list(map(update_review_date, employees_to_review))
                return "Email was sent successfully!"
        else:
            return "There is no employees to review"

