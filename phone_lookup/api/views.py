from django.shortcuts import render
# api/views.py

from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User, Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegistrationForm
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SpamReport
from .forms import SpamReportForm
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect(reverse('login'))  # Redirect to login after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

#to create teh register page..

# @login_required
def report_spam_view(request):
    if request.method == 'POST':
        form = SpamReportForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            # Create a new spam report
            SpamReport.objects.create(phone_number=phone_number, reported_by=request.user)
            return redirect('spam_report_success')  # Redirect to success page after submission
    else:
        form = SpamReportForm()

    return render(request, 'report_spam.html', {'form': form})

def spam_report_success_view(request):
    return render(request, 'spam_report_success.html')

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        # Use .get() to handle missing fields gracefully
        phone_number = data.get('phone_number')
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')

        if not phone_number or not name or not password:
            return Response({"error": "Phone number, name, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            phone_number=phone_number,
            name=name,
            password=password,
            email=email
        )
        return Response(UserSerializer(user).data)

#to create the login feature..
class LoginView(APIView):
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            return Response(UserSerializer(user).data)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class SpamReportView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpamReportSerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        SpamReport.objects.create(phone_number=phone_number, reported_by=request.user)
        return Response({"detail": "Spam reported"})

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        if query.isdigit():  # Phone number search
            contacts = Contact.objects.filter(phone_number=query)
        else:  # Name search
            contacts = Contact.objects.filter(name__icontains=query).order_by('name')
        
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

# Create your views here.
