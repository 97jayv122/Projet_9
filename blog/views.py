from django.conf import settings
from django.core.paginator import Paginator
from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from . import forms, models


User = get_user_model()

@login_required
def home(request):
    """
    Display the blog homepage with a paginated feed of tickets and reviews.

    - Retrieves users the current user follows (including self) and handles block lists.
    - Queries tickets and reviews by these users, excluding blocked ones.
    - Merges and sorts results by creation time (newest first).
    - Paginates the combined list (6 items per page).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'blog/home.html' with context {'page_obj'}.
    """
    following = list(request.user.follows.all()) + [request.user]
    blocked = request.user.blocked.all()
    blocked_by = request.user.blocked_by.all()
    tickets = models.Ticket.objects.filter(user__in=following)\
                                    .exclude(user__in=blocked)\
                                    .exclude(user__in=blocked_by)
    reviews = models.Review.objects.filter(
        Q(user__in=following) | Q(ticket__user=request.user)
    ).exclude(user__in=blocked).exclude(user__in=blocked_by)

    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance : instance.time_created,
        reverse=True
    )
    paginator = Paginator(tickets_and_reviews, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'show_edit': False,
    }
    return render(request,
                  'blog/home.html', context=context)

@login_required
def display_posts(request):
    """
    Display the current user's tickets and reviews.

    - Fetches tickets and reviews created by the user.
    - Merges and sorts them by creation time (newest first).
    - Paginates the list (6 items per page).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'blog/posts.html' with context {'page_obj'}.
    """
    tickets = models.Ticket.objects.filter(
        user=request.user
    )
    reviews = models.Review.objects.filter(
        user=request.user
    )
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance : instance.time_created,
        reverse=True
    )
    paginator = Paginator(tickets_and_reviews, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'show_edit': True,
    }
    return render(request,
                  'blog/posts.html', context=context)

@login_required
def create_review(request, ticket_id):
    """
    Create a review for an existing ticket.

    - Displays an empty ReviewForm or processes a submitted form.
    - Associates the new review with the current user and specified ticket.

    Args:
        request (HttpRequest): The HTTP request object.
        ticket_id (int): Primary key of the ticket to review.

    Returns:
        HttpResponse: Renders 'blog/create_review.html' or redirects to 'view-review'.
    """
    ticket = (get_object_or_404(models.Ticket, id=ticket_id))
    review_form = forms.ReviewForm()
    if request.method == 'POST':    
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('view-review', review.id)
    return render(request,
                  'blog/create_review.html', context={
                      'ticket': ticket,
                      'review_form': review_form
                  })

@login_required
def edit_ticket(request, ticket_id):
    """
    Edit or delete an existing ticket owned by the user.

    - If 'edit_ticket' in POST: validate and save changes.
    - If 'delete_ticket' in POST: validate and delete the ticket.

    Args:
        request (HttpRequest): The HTTP request object.
        ticket_id (int): Primary key of the ticket to edit.

    Returns:
        HttpResponse: Renders 'blog/edit_ticket.html' or redirects on success.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if ticket_form.is_valid():
                ticket_form.save()
                return redirect(settings.LOGIN_REDIRECT_URL)
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid:
                ticket.delete()
                return redirect(settings.LOGIN_REDIRECT_URL)
    context={
        'ticket_form':ticket_form,
        'delete_form': delete_form
    }
    return render(request, 'blog/edit_ticket.html', context=context)

@login_required
def edit_review(request, review_id):
    """
    Edit or delete an existing review owned by the user.

    - If 'edit_review' in POST: validate and save changes.
    - If 'delete_review' in POST: validate and delete the review.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): Primary key of the review to edit.

    Returns:
        HttpResponse: Renders 'blog/edit_review.html' or redirects on success.
    """
    review = get_object_or_404(models.Review, id=review_id)
    review_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            review_form = forms.ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('view-review', review.id)
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid:
                review.delete
                return redirect(settings.LOGIN_REDIRECT_URL)
    context={
        'review_form':review_form,
        'review': review,
        'delete_form': delete_form
    }
    return render(request, 'blog/edit_review.html', context=context)

@login_required
def create_ticket_and_review(request):
    """
    Create both a ticket and its initial review in a single form.

    - Displays two forms (TicketForm and ReviewForm) with prefixes.
    - On POST, validates and saves both objects, linking them correctly.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'blog/create_ticket_and_review.html' or redirects.
    """
    ticket_form = forms.TicketForm(prefix='ticket')
    review_form = forms.ReviewForm(prefix='review')
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES, prefix='ticket')
        review_form = forms.ReviewForm(request.POST, prefix='review')
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/create_ticket_and_review.html', {
        'ticket_form': ticket_form,
        'review_form': review_form,
    })

@login_required
def view_ticket(request, ticket_id):
    """
    Display details of a single ticket.

    Args:
        request (HttpRequest): The HTTP request object.
        ticket_id (int): Primary key of the ticket to view.

    Returns:
        HttpResponse: Renders 'blog/view_ticket.html' with {'ticket'}.
    """
    ticket = (get_object_or_404(models.Ticket, id=ticket_id))
    return render(request,
                  'blog/view_ticket.html', {
                      'ticket': ticket,
                      'show_edit': True
                      })

@login_required
def create_ticket(request):
    """
    Create a new ticket.

    - Displays TicketForm or processes it on POST.
    - Associates the new ticket with the current user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'blog/create_ticket.html' or redirects.
    """
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
                  'blog/create_ticket.html', context={'ticket_form': ticket_form})

@login_required
def view_review(request, review_id):
    """
    Display details of a single review.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): Primary key of the review to view.

    Returns:
        HttpResponse: Renders 'blog/view_review.html' with {'review'}.
    """
    review = (get_object_or_404(models.Review, id=review_id))
    return render(request,
                  'blog/view_review.html', context={
                      'review': review,
                      'show_edit': True
                  })

@login_required
def follow_users(request):
    """
    Manage following/unfollowing other users.

    - Displays FollowUsersForm to select users to follow.
    - Saves changes and redirects to homepage.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'blog/follow_users_form.html' with {'form'}.
    """
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('follow_users')
    return render(request,
                  'blog/follow_users_form.html', context={
                      'form': form,
                      })

@login_required
def unfollow_users(request, user_id):
    """
    Unfollow a specific user.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): Primary key of the user to unfollow.

    Returns:
        HttpResponse: Redirects to 'follow_users' view.
    """
    target_user = get_object_or_404(User, id=user_id)
    request.user.follows.remove(target_user)
    return redirect('follow_users')

@login_required
def blocked_users(request, user_id):
    """
    Block the specified user for the current user.

    Retrieves the target user by ID, adds them to the
    current user's blocked list, and then redirects
    back to the follow users page.
    """
    target_user = get_object_or_404(User, id=user_id)
    request.user.blocked.add(target_user)
    return redirect('follow_users')
    
@login_required
def unblocked_users(request, user_id):
    """
    Unblock the specified user for the current user.

    Retrieves the target user by ID, removes them from the
    current user's blocked list, and then redirects
    back to the follow users page.
    """
    target_user = get_object_or_404(User, id=user_id)
    request.user.blocked.remove(target_user)
    return redirect('follow_users')