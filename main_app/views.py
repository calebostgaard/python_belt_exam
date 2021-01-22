from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.user_validator(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashed_pw)
        new_user = User.objects.create(
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        request.session['user_id'] = new_user.id
        return redirect("/dashboard")

def log_in(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect("/dashboard")
        messages.error(request, "** Invalid Credentials **")
        return redirect("/")
    messages.error(request, "** Email is not associated with an account, please register **")
    return redirect("/")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')
    user_id = int(request.session['user_id'])
    specified_user = User.objects.get(id=int(user_id))
    context = {
        "all_trips" : Trip.objects.filter(users_who_joined = specified_user).order_by("-created_at"),
        "other_trips" : Trip.objects.exclude(users_who_joined = specified_user).order_by("-created_at"),
        "specified_user" : User.objects.get(id=user_id),
    }
    return render(request, "welcome.html", context)

def new_trip(request):
    if "user_id" not in request.session:
        return redirect('/')
    user_id = int(request.session['user_id'])
    context = {
        "specified_user" : User.objects.get(id=user_id),
    }
    return render(request, "new_trip.html", context)

def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        user_id = int(request.session['user_id'])
        new_trip = Trip.objects.create(
            destination = request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan = request.POST['plan'],
            created_by = User.objects.get(id=user_id),
        )
        this_user = User.objects.get(id=user_id)
        this_user.trips_joined.add(new_trip)
        return redirect("/dashboard")

def delete_trip(request, num):
    this_trip = Trip.objects.get(id=num)
    this_trip.delete()
    return redirect("/dashboard")

def edit_trip(request, num):
    user_id = int(request.session['user_id'])
    this_trip = Trip.objects.get(id=num)
    this_start_date = this_trip.start_date.strftime("%Y-%m-%d")
    this_end_date = this_trip.end_date.strftime("%Y-%m-%d")
    context = {
            "specific_trip": Trip.objects.get(id=num),
            "this_start_date" : this_start_date,
            "this_end_date" : this_end_date,
            "specified_user" : User.objects.get(id=user_id),

    }
    
    return render(request, "edit_trip.html", context)

def edit_trip_execute(request, num):
    errors = Trip.objects.trip_validator(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'/trips/edit/{num}')
    else:
        trip_to_edit = Trip.objects.get(id=int(num))
        trip_to_edit.destination = request.POST['destination']
        trip_to_edit.start_date = request.POST['start_date']
        trip_to_edit.end_date = request.POST['end_date']
        trip_to_edit.plan = request.POST['plan']
        trip_to_edit.save()
        return redirect("/dashboard")

def view_trip(request, num):
    if "user_id" not in request.session:
        return redirect('/')
    user_id = int(request.session['user_id'])
    specified_trip = Trip.objects.get(id=num)
    these_users = User.objects.filter(trips_joined = specified_trip)
    my_list = these_users.exclude(trips_created=specified_trip)
    print(my_list)
    context = {
        "specified_user" : User.objects.get(id=user_id),
        "specified_trip" : Trip.objects.get(id=num),
        "specified_joiners" : these_users,
        "my_list" : my_list,
    }
    return render(request, "view_trip.html", context)

def join_trip(request, num):
    user_id = int(request.session['user_id'])
    this_user = User.objects.get(id=user_id)
    this_trip = Trip.objects.get(id=num)
    this_user.trips_joined.add(this_trip)
    return redirect('/dashboard')

def cancel_trip(request, num):
    user_id = int(request.session['user_id'])
    this_user = User.objects.get(id=user_id)
    this_trip = Trip.objects.get(id=num)
    this_user.trips_joined.remove(this_trip)
    return redirect('/dashboard')

def log_out(request):
    del request.session['user_id']
    return redirect('/')