"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import authentication.forms
import authentication.views
import blog.views
from authentication.forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView,PasswordChangeDoneView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        authentication_form=CustomAuthenticationForm,
        redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', blog.views.home, name='home'),
    path('passwordchange/', PasswordChangeView.as_view(
        template_name='authentication/registration.html',
        success_url='passwordchanged'
    ),
         name='passwordchange'),
    path('passwordchanged/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'
    ),
         name='passwordchanged'),
    path('signup/',authentication.views.signup, name='signup'),
    path('photo/profile/upload', authentication.views.upload_profile_photo,
         name='profile_photo_upload'),
    path('create/ticket', blog.views.create_ticket, name="create-ticket"),
    path('ticket/<int:ticket_id>/create/review', blog.views.create_review,
          name='create-review'),
    path('create/review-ticket', blog.views.create_ticket_and_review,
          name='create-review-ticket'),
    path('review/<int:review_id>', blog.views.view_review,
         name='view-review'),
    path('follow-users', blog.views.follow_users, name='follow_users'),
    path('unfollow/<int:user_id>/', blog.views.unfollow_users,
          name='unfollow_users'),
    path('posts', blog.views.display_posts, name='posts'),
    path('edit/ticket/<int:ticket_id>', blog.views.edit_ticket, name='edit_ticket'),
    path('edit/review/<int:review_id>', blog.views.edit_review, name='edit_review'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
