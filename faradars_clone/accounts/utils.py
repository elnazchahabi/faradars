# accounts/utils.py
from orders.models import OrderItem
from courses.models import Course
from django.contrib.contenttypes.models import ContentType

def get_user_courses(user):
    course_type = ContentType.objects.get_for_model(Course)
    items = OrderItem.objects.filter(
        content_type=course_type,
        order__user=user,
        order__is_paid=True
    )
    return [item.item_object for item in items]
