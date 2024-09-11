# api/urls.py

from django.urls import path
from .views import RegisterView, LoginView, SpamReportView, SearchView
from django.contrib.auth import views as auth_views
from api.views import register_view ,report_spam_view, spam_report_success_view
from api.forms import CustomAuthenticationForm

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=CustomAuthenticationForm ), name='login'), 
    # Add the report-spam URL
    path('login/report-spam/', report_spam_view, name='report_spam'),

    # Success page after submitting spam report
    path('report-spam/success/', spam_report_success_view, name='spam_report_success'),
    path('search/', SearchView.as_view(), name='search'),
]
