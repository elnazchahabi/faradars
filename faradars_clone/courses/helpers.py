from orders.models import OrderItem

# def user_has_course(user, course):
#     if not user.is_authenticated:
#         return False
#     return OrderItem.objects.filter(order__user=user, order__is_paid=True, course=course).exists()


from django.contrib.contenttypes.models import ContentType

def user_has_course(user, course):
    return OrderItem.objects.filter(
        order__user=user,
        order__is_paid=True,
        content_type=ContentType.objects.get_for_model(course.__class__),
        object_id=course.id
    ).exists()
