from django.contrib import admin
from .models import SupportTicket, TicketMessage

class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    fields = ('message', 'sender', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['sender']

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'status', 'created_at')
    search_fields = ('user__username', 'subject')
    list_filter = ('status', 'created_at')
    readonly_fields = ('user', 'subject', 'created_at')
    ordering = ('-created_at',)
    inlines = [TicketMessageInline]

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'created_at')
    search_fields = ('ticket__subject', 'sender__username', 'message')

