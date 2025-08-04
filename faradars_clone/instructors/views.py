from django.shortcuts import render, get_object_or_404
from .models import Instructor
from courses.models import Course
from blog.models import Post

def instructor_profile(request, username):
    instructor = get_object_or_404(Instructor, user__username=username)
    courses    = Course.objects.filter(instructor=instructor)
    # ← این خط را اضافه می‌کنیم:
    posts      = Post.objects.filter(author=instructor.user).order_by('-published_date')

    return render(request, 'instructors/profile.html', {
        'instructor': instructor,
        'courses':    courses,
        'posts':      posts,    # ← حالا posts تعریف شده و پاس داده می‌شود
    })
