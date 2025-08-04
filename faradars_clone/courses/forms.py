### courses/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import Q

from .models import Course, Lesson, CourseReview, Category, Tag,CourseQuestion, CourseAnswer
from instructors.models import Instructor



class SearchForm(forms.Form):
    q = forms.CharField(label='جستجو', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="دسته‌بندی")
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label="تگ")
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.all(), required=False, label="مدرس")
    price = forms.ChoiceField(
        choices=[
            ('', 'همه'),
            ('free', 'رایگان'),
            ('paid', 'پولی'),
        ],
        required=False,
        label="نوع دوره"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','slug','description','price','category','tags','thumbnail','prerequisites')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ذخیره'))

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title','video','is_preview','order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ذخیره درس'))

class CourseReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i,i) for i in range(1,6)], label='امتیاز')

    class Meta:
        model = CourseReview
        fields = ('rating','comment')
        widgets = {'comment': forms.Textarea(attrs={'rows':3})}
        labels = {'comment': 'نظر شما'}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['user'] = user
            self.initial['course'] = course
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ارسال نظر'))

    def clean(self):
        cleaned = super().clean()
        if not self.instance.pk:
            user = self.initial.get('user')
            course = self.initial.get('course')
            if CourseReview.objects.filter(user=user, course=course).exists():
                raise forms.ValidationError('شما قبلاً برای این دوره نظر داده‌اید.')
        return cleaned
    


class SearchForm(forms.Form):
    q = forms.CharField(label='جستجو', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="دسته‌بندی")
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label="تگ")
    price = forms.ChoiceField(
        choices=(
            ('', 'همه'),
            ('free', 'رایگان'),
            ('paid', 'پولی'),
        ),
        required=False,
        label="نوع دوره"
    )






class CourseReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        label='امتیاز (۱ تا ۵)'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='نظر شما'
    )
    class Meta:
        model = CourseReview
        fields = ('rating', 'comment')
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned = super().clean()
        # فقط یک نظر برای هر کاربر و هر دوره
        if self.user and self.course and not self.instance.pk:
            if CourseReview.objects.filter(user=self.user, course=self.course).exists():
                raise forms.ValidationError("شما قبلاً برای این دوره نظر داده‌اید.")
        return cleaned


class CourseQuestionForm(forms.ModelForm):
    class Meta:
        model = CourseQuestion
        fields = ['question']

class CourseAnswerForm(forms.ModelForm):
    class Meta:
        model = CourseAnswer
        fields = ['answer']






class CourseQuestionForm(forms.ModelForm):
    class Meta:
        model = CourseQuestion
        fields = ['question']
        labels = {'question': 'سوال شما'}

class CourseAnswerForm(forms.ModelForm):
    class Meta:
        model = CourseAnswer
        fields = ['answer']
        labels = {'answer': 'پاسخ'}
