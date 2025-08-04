# Register your models here.
from django.contrib import admin
from .models import InstructorRequest
from django.contrib import admin
from .models import Instructor, InstructorRequest


@admin.register(InstructorRequest)
class InstructorRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'expertise', 'is_checked', 'created_at')
    list_filter = ('is_checked',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        # اگه تأیید شد، کاربر مدرس بشه
        if obj.is_approved and not obj.user.is_instructor:
            obj.user.is_instructor = True
            obj.user.save()
        super().save_model(request, obj, form, change)



@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')


