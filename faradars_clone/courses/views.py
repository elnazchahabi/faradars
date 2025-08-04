



# Create your views here.
from django.http import HttpResponse
from instructors.models import Instructor
from .models import Course, Category ,CourseReview, Lesson, Tag,CourseQuestion, CourseAnswer
from .forms import SearchForm,CourseReviewForm,CourseQuestionForm, CourseAnswerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course
from orders.models import Order  # اگر اپ orders اینجاست
from .helpers import user_has_course  # اگر تو helpers نوشتی، وگرنه همینجا تعریف 
from django.db.models import Q
from .models import Lesson

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required





def course_list(request):
    courses = Course.objects.all()
    form = SearchForm(request.GET or None)

    # فیلتر از فرم جستجو
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        tag = form.cleaned_data.get('tag')
        instructor = form.cleaned_data.get('instructor')
        price = form.cleaned_data.get('price')

        if q:
            courses = courses.filter(title__icontains=q)
        if category:
            courses = courses.filter(category=category)
        if tag:
            courses = courses.filter(tags=tag)
        if instructor:
            courses = courses.filter(instructor=instructor)
        if price == 'free':
            courses = courses.filter(price=0)
        elif price == 'paid':
            courses = courses.exclude(price=0)


    # مرتب‌سازی
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        courses = courses.order_by('price')
    elif sort == 'price_desc':
        courses = courses.order_by('-price')
    elif sort == 'rating':
        courses = sorted(courses, key=lambda c: c.average_rating(), reverse=True)
    else:
        courses = courses.order_by('-created_at')  # جدیدترین پیش‌فرض


        # صفحه‌بندی: 10 دوره در هر صفحه

    paginator = Paginator(courses, 10)
    page = request.GET.get('page', 1)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'form': form,
    })




def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all()
    reviews = course.reviews.select_related('user').all()
    has_course = user_has_course(request.user, course)

    # --- فرم نظر
    review_form = None
    if request.user.is_authenticated:
        if not CourseReview.objects.filter(user=request.user, course=course).exists():
            review_form = CourseReviewForm(data=request.POST or None, user=request.user, course=course)
            if request.method == "POST" and 'submit_review' in request.POST and review_form.is_valid():
                review = review_form.save(commit=False)
                review.course = course         # 👈 مقداردهی کلیدی
                review.user = request.user     # 👈 اگه لازم داری، معمولا مهمه!
                review.save()
                messages.success(request, "نظر شما ثبت شد.")
                return redirect('courses:course_detail', slug=slug)




    # --- فرم پرسش و پاسخ
    q_form = CourseQuestionForm()
    a_form = CourseAnswerForm()

    if request.method == 'POST':
        # ارسال سوال
        if 'question_submit' in request.POST:
            q_form = CourseQuestionForm(request.POST)
            if q_form.is_valid():
                q = q_form.save(commit=False)
                q.user = request.user
                q.course = course
                q.save()
                messages.success(request, "سوال با موفقیت ثبت شد.")
                return redirect('courses:course_detail', slug=slug)

        # ارسال پاسخ
        elif 'answer_submit' in request.POST:
            a_form = CourseAnswerForm(request.POST)
            question_id = request.POST.get('question_id')
            if a_form.is_valid() and question_id:
                a = a_form.save(commit=False)
                a.user = request.user
                a.question_id = question_id
                a.save()
                messages.success(request, "پاسخ ثبت شد.")
                return redirect('courses:course_detail', slug=slug)

    # دوره‌های مشابه (بر اساس دسته یا تگ)
    similar_courses = Course.objects.filter(
        Q(category=course.category) | Q(tags__in=course.tags.all())
    ).exclude(id=course.id).distinct()


    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'form': review_form,
        'has_course': has_course,
        'q_form': q_form,
        'a_form': a_form,
        'questions': course.questions.prefetch_related('answers'),
        'similar_courses': similar_courses,
    })



def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    # اگر بعداً نیاز به چک خرید یا دسترسی داشتیم، اینجا می‌آوریم:
    # has_access = user_has_course(request.user, lesson.course) or lesson.is_preview
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        # 'has_access': has_access,
    })



def all_tags(request):
    tags = Tag.objects.all()
    return render(request, 'courses/all_tags.html', {'tags': tags})




def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'courses/all_categories.html', {
        'categories': categories
    })


def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_courses.html', {
        'category': category,
        'courses': courses
    })




def tag_courses(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    courses = Course.objects.filter(tags=tag)
    return render(request, 'courses/tag_courses.html', {
        'tag': tag,
        'courses': courses
    })







from .models import UserCourseProgress

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user, is_paid=True).select_related('course').order_by('-created_at')
    course_progresses = {p.course_id: p for p in UserCourseProgress.objects.filter(user=request.user)}

    courses_data = []
    for order in orders:
        course = order.course
        progress = course_progresses.get(course.id)
        percentage = progress.progress_percentage() if progress else 0
        courses_data.append({
            'course': course,
            'percentage': percentage,
        })

    return render(request, 'courses/dashboard.html', {
        'courses_data': courses_data
    })
