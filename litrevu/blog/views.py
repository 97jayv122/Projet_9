from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
# Create your views here.
@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request,
                  'blog/home.html', context={
                      'tickets': tickets,
                      'reviews': reviews
                      })

@login_required
def create_review(request, ticket_id):
    ticket = (get_object_or_404(models.Ticket, id=ticket_id))
    review_form = forms.ReviewForm()
    if request.method == 'POST':    
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    return render(request,
                  'blog/create_review.html', context={
                      'ticket': ticket,
                      'review_form': review_form
                  })

@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.uploader = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request,
                  'blog/create_ticket_and_review.html', context=context)

@login_required
def view_ticket(request, ticket_id):
    ticket = (get_object_or_404(models.Ticket, id=ticket_id))
    return render(request,
                  'blog/view_ticket', {'ticket': ticket})

@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.uploader = request.user
            ticket.save()
            return redirect('home')
    return render(request,
                  'blog/create_ticket.html', context={'form': form})

@login_required
def view_review(request, ticket_id, review_id):
    ticket = (get_object_or_404(models.Ticket, id=ticket_id))
    review = (get_object_or_404(models.Review, id=review_id))
    return render(request,
                  'blog/view_review.html', context={
                      'ticket': ticket,
                      'review': review
                  })

@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,
                  'blog/follow_users_form.html', context={'form': form})
