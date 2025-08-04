from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.views.generic import UpdateView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from .forms import InstructorRequestForm, MobileRequestForm, OTPVerifyForm, ProfileForm
from .models import LoginHistory, CustomUser, MobileOTP
from instructors.models import InstructorRequest, Instructor
from courses.models import Course, UserCourseProgress
from store.models import Product
from django.contrib.contenttypes.models import ContentType
from .models import Wallet, WalletTransaction
from .forms import WalletChargeForm

User = get_user_model()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "پروفایل شما با موفقیت به‌روزرسانی شد.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_history'] = LoginHistory.objects.filter(user=self.request.user).order_by('-login_time')[:10]
        context['instructor_request'] = InstructorRequest.objects.filter(user=self.request.user).order_by('-id').first()
        context['is_instructor'] = getattr(self.request.user, 'is_instructor', False)
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['orders'] = Order.objects.filter(user=user).order_by('-created_at')
        context['instructor_request'] = InstructorRequest.objects.filter(user=user).order_by('-id').first()
        context['is_instructor'] = getattr(user, 'is_instructor', False)

        try:
            instructor_obj = Instructor.objects.get(user=user)
            context['instructor_courses'] = Course.objects.filter(instructor=instructor_obj)
        except Instructor.DoesNotExist:
            context['instructor_courses'] = []

        context['recent_logins'] = LoginHistory.objects.filter(user=user).order_by('-login_time')[:5]

        # دوره‌های خریداری‌شده با پیشرفت
        course_type = ContentType.objects.get_for_model(Course)
        bought_items = OrderItem.objects.filter(
            content_type=course_type,
            order__user=user,
            order__is_paid=True
        )
        courses = [item.item_object for item in bought_items]
        course_progress = {
            progress.course_id: progress.progress_percentage()
            for progress in UserCourseProgress.objects.filter(user=user)
        }
        bought_courses_data = []
        for course in courses:
            bought_courses_data.append({
                'course': course,
                'first_lesson': course.lessons.first(),
                'percentage': course_progress.get(course.id, 0)
            })
        context['bought_courses'] = bought_courses_data

        wallet, _ = Wallet.objects.get_or_create(user=user)
        context['wallet'] = wallet
        return context

class DeactivateAccountView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, "حساب کاربری شما غیرفعال شد. برای بازگردانی، با پشتیبانی تماس بگیرید.")
        return redirect('account_logout')

class InstructorRequestView(LoginRequiredMixin, CreateView):
    model = InstructorRequest
    form_class = InstructorRequestForm
    template_name = 'accounts/teacher_request.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        if InstructorRequest.objects.filter(user=self.request.user).exists():
            messages.error(self.request, "شما قبلاً درخواست داده‌اید.")
            return redirect('dashboard')
        form.instance.user = self.request.user
        messages.success(self.request, "درخواست شما ثبت شد و بررسی خواهد شد.")
        return super().form_valid(form)

def mobile_signup_request(request):
    if request.method == "POST":
        form = MobileRequestForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            user, created = CustomUser.objects.get_or_create(mobile=mobile, defaults={'username': mobile})
            code = MobileOTP.generate_otp()
            MobileOTP.objects.create(user=user, code=code)
            messages.success(request, f"کد تایید: {code}")
            request.session['otp_mobile'] = mobile
            return redirect('otp_verify')
    else:
        form = MobileRequestForm()
    return render(request, "accounts/mobile_signup.html", {"form": form})

def otp_verify(request):
    mobile = request.session.get('otp_mobile')
    if not mobile:
        return redirect('mobile_signup')

    user = CustomUser.objects.get(mobile=mobile)
    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            otp = MobileOTP.objects.filter(user=user, code=code, is_used=False).order_by('-created_at').first()
            if otp:
                otp.is_used = True
                otp.save()
                user.is_mobile_verified = True
                user.save()
                messages.success(request, "حساب شما با موفقیت فعال شد!")
                return redirect('dashboard')
            else:
                messages.error(request, "کد وارد شده اشتباه است یا قبلا استفاده شده")
    else:
        form = OTPVerifyForm()
    return render(request, "accounts/otp_verify.html", {"form": form, "mobile": mobile})

class WalletChargeView(LoginRequiredMixin, View):
    def get(self, request):
        form = WalletChargeForm()
        wallet = request.user.wallet
        return render(request, 'accounts/wallet_charge.html', {'form': form, 'wallet': wallet})

    def post(self, request):
        form = WalletChargeForm(request.POST)
        wallet = request.user.wallet
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet.balance += amount
            wallet.save()
            WalletTransaction.objects.create(
                wallet=wallet,
                transaction_type='charge',
                amount=amount,
                description='شارژ دستی کیف پول'
            )
            messages.success(request, "کیف پول با موفقیت شارژ شد.")
            return redirect('dashboard')
        return render(request, 'accounts/wallet_charge.html', {'form': form, 'wallet': wallet})
