from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SupportTicket, TicketMessage
from .forms import SupportTicketForm, TicketMessageForm

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_create(request):
    if request.method == "POST":
        ticket_form = SupportTicketForm(request.POST)
        message_form = TicketMessageForm(request.POST)
        if ticket_form.is_valid() and message_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            msg = message_form.save(commit=False)
            msg.ticket = ticket
            msg.sender = request.user
            msg.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        ticket_form = SupportTicketForm()
        message_form = TicketMessageForm()
    return render(request, 'support/ticket_create.html', {
        'ticket_form': ticket_form,
        'message_form': message_form
    })

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if not (request.user == ticket.user or request.user.is_staff):
        return redirect('ticket_list')
    form = TicketMessageForm()
    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket, 'form': form, 'user': request.user
    })

@login_required
@csrf_exempt
def ticket_send_message(request, pk):
    if request.method == 'POST':
        ticket = get_object_or_404(SupportTicket, pk=pk)
        if not (request.user == ticket.user or request.user.is_staff) or ticket.status == "closed":
            return JsonResponse({'error': 'دسترسی ندارید یا تیکت بسته است'}, status=403)
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ticket = ticket
            msg.sender = request.user
            msg.save()
            # تغییر وضعیت تیکت
            if request.user.is_staff:
                ticket.status = 'answered'
            else:
                ticket.status = 'pending'
            ticket.save()
            return JsonResponse({
                'id': msg.id,
                'message': msg.message,
                'sender': 'پشتیبانی' if request.user.is_staff else request.user.username,
                'created_at': msg.created_at.strftime("%Y/%m/%d %H:%M"),
                'is_staff': request.user.is_staff
            })
        return JsonResponse({'error': 'فرم نامعتبر'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

@login_required
def ticket_messages_api(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if not (request.user == ticket.user or request.user.is_staff):
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)
    messages = ticket.messages.all().order_by('created_at')
    data = []
    for msg in messages:
        data.append({
            'id': msg.id,
            'message': msg.message,
            'sender': 'پشتیبانی' if msg.sender.is_staff else msg.sender.username,
            'created_at': msg.created_at.strftime("%Y/%m/%d %H:%M"),
            'is_staff': msg.sender.is_staff
        })
    return JsonResponse({'messages': data})





from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_ticket_list(request):
    tickets = SupportTicket.objects.all().order_by('-created_at')
    return render(request, 'support/admin_ticket_list.html', {'tickets': tickets})

@staff_member_required
def admin_ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    form = TicketMessageForm()
    return render(request, 'support/admin_ticket_detail.html', {
        'ticket': ticket, 'form': form, 'user': request.user
    })

@staff_member_required
@csrf_exempt
def admin_ticket_send_message(request, pk):
    if request.method == 'POST':
        ticket = get_object_or_404(SupportTicket, pk=pk)
        if ticket.status == "closed":
            return JsonResponse({'error': 'تیکت بسته است'}, status=403)
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ticket = ticket
            msg.sender = request.user  # پشتیبان
            msg.save()
            ticket.status = 'answered'
            ticket.save()
            return JsonResponse({
                'id': msg.id,
                'message': msg.message,
                'sender': 'پشتیبانی',
                'created_at': msg.created_at.strftime("%Y/%m/%d %H:%M"),
                'is_staff': True
            })
        return JsonResponse({'error': 'فرم نامعتبر'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

@staff_member_required
def close_ticket(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    ticket.status = 'closed'
    ticket.save()
    return redirect('admin_ticket_detail', pk=ticket.pk)
