from django.shortcuts import render, redirect
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Message, UserChannel
from django.db.models import Q


class Main(View):
    """Display the main landing page and redirect authenticated users to the home page."""
    def get(self, request):
        """Render the main page for unauthenticated users."""
   
        if request.user.is_authenticated:
            return redirect("home")
        return render(request=request, template_name="chat/main.html")


class Login(View):
    """Handle user authentication and display the login page."""
    def get(self, request):
        """Render the login page."""
        return render(request=request, template_name="chat/login.html")

    def post(self, request):
        """Authenticate the submitted credentials and log the user in if valid."""
        data = request.POST.dict()
        try:
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request=request, username=username, password=password)
            print(user)
            if user:
                login(request=request, user=user)
                return redirect("home")
            else:
                raise Exception
        except:
            context = {"error": "sth is wrong"}
            return render(
                request=request, template_name="chat/login.html", context=context
            )


class Register(View):
    """Handle new user registration and automatically log in registered users."""
    def get(self, request):
        """Render the user registration page."""
        return render(request=request, template_name="chat/register.html")

    def post(self, request):
        """Create a new user account from the submitted registration data."""
        context = {}
        data = request.POST.dict()
        try:
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                username=username,
            )
            user = authenticate(request=request, username=username, password=password)
            print(user)
            if user:
                login(request=request, user=user)
                return redirect("home")
        except:
            context.update({"error": "data is wrong"})

        return render(
            request=request, template_name="chat/register.html", context=context
        )


class Logout(View):
    """Log out the current user and redirect them to the main page."""
    def get(self, request):
        """Log out the current user."""
        logout(request)
        return redirect("main")


class Home(View):
    """Display the authenticated user's home page and available users."""
    def get(self, request):
        """Render the home page for authenticated users."""
        if request.user.is_authenticated:
            users = User.objects.all()
            context = {"user": request.user, "users": users}
            return render(
                request=request, template_name="chat/home.html", context=context
            )
        return redirect("main")


class ChatPerson(View):
    """Display a conversation between the authenticated user and another user."""
    def get(self, request, id):
        """Retrieve and display exchanged messages and mark received messages as seen."""
 
        person = User.objects.get(id=id)
        print(person)

        me = request.user
        
        messages = Message.objects.filter(
            Q(sender=me, reciever=person) | Q(sender=person,reciever=me)
        ).order_by("date", "time")

    
        not_seen_messages = Message.objects.filter(sender=person, reciever=me)
        not_seen_messages.update(has_been_seen=True)

        context = {"person": person, "me": me, "messages": messages}
        return render(
            request=request, template_name="chat/chat_person.html", context=context
        )
