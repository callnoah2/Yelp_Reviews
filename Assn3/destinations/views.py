from django.shortcuts import render, redirect
from .models import Destination
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    return render(request, 'index.html', {'destinations': destinations})

def newUsers(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Fix the key to retrieve email
        password = request.POST.get('password')

        # Check if the email is valid
        if '@' not in email:
            return HttpResponseBadRequest("Invalid email format")

        # Check if the password is valid
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return HttpResponseBadRequest("Password should be at least 8 characters and contain a number")

        # Create the user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('destinations')
        except:
            return HttpResponseBadRequest("User creation failed")

    return render(request, 'newUser.html')

def newSessions(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('destinations')  # assuming you have a 'destinations' path configured in your urls.py

    return render(request, 'newSessions.html')

def users(request):
    return HttpResponse("users.html")

def sessions(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('destinations')  # assuming you have a 'destinations' path configured in your urls.py

    return render(request, 'sessions.html')

@login_required
def sessionsDestroy(request):
    logout(request)  # Destroys the current user's session
    return redirect('/')

def destinations(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        share_publicly = request.POST.get('share_publicly')

        # Convert share_publicly to a boolean
        share_publicly = share_publicly.lower() == 'true'

        # Create the destination with the current user
        user = request.user  # get the current user
        new_destination = Destination.objects.create(
            name=name,
            review=review,
            rating=rating,
            share_publicly=share_publicly,
            user=user  # associate the user with the destination
        )
        # Redirect to /destinations
        return redirect('destinations')
    
    user_destinations = Destination.objects.filter(user=request.user)
    return render(request, 'destinations.html', {'destinations': user_destinations})

@login_required
def newDestinations(request):
    return render(request, 'newDestinations.html')

@login_required
def destinationsId(request, id):
    try:
        destination = Destination.objects.get(pk=id)
        if destination.user == request.user:
            return render(request, 'editDestinations.html', {'destination': destination})
        else:
            return HttpResponse(status=404)  # Respond with 404 if the user doesn't own the destination
    except Destination.DoesNotExist:
        return HttpResponse(status=404)  # Respond with 404 if the destination doesn't exist

@login_required
def updateDestination(request, id):
    try:
        destination = Destination.objects.get(pk=id)
        if destination.user == request.user:
            if request.method == 'POST':
                # Update the destination with the form data
                destination.name = request.POST.get('name')
                destination.review = request.POST.get('review')
                destination.rating = request.POST.get('rating')

                # Check if the share_publicly checkbox is selected
                share_publicly_value = request.POST.get('share_publicly')
                if share_publicly_value == 'true':
                    destination.share_publicly = True
                else:
                    destination.share_publicly = False

                destination.save()
                return redirect('destinations')  # Redirect to destinations after successful update
            else:
                return HttpResponse(status=405)  # Method Not Allowed
        else:
            return HttpResponse(status=404)  # Respond with 404 if the user doesn't own the destination
    except Destination.DoesNotExist:
        return HttpResponse(status=404)  # Respond with 404 if the destination doesn't exist

@login_required
def destroyDestinationsId(request, id):
    try:
        destination = Destination.objects.get(pk=id)
        if destination.user == request.user:
            destination.delete()
            return redirect('destinations')  # Redirect to /destinations after successful deletion
        else:
            raise Http404()  # Raise 404 if the user doesn't own the destination
    except Destination.DoesNotExist:
        raise Http404()  # Raise 404 if the destination doesn't exist
