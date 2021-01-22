from django.db import models
import re
from datetime import date, datetime, timedelta


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors["fname"] = "** First name should be at least 2 characters **"
        if len(postData['lname']) < 2:
            errors["lname"] = "** Last name should be at least 2 characters **"
        for users in User.objects.filter(email = postData['email']):
            if users.email == postData['email']:
                errors["unique_email"] = "** Email has already been used, please login or try another **"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "** Invalid email address format **"
        if len(postData['password']) < 8:
            errors["password"] = "** Password should be at least 8 characters **"
        if postData['password'] != postData['checkPassword']:
            errors["checkPassword"] = "** Passwords must match **"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    # trips_created = a list of trips create by this user
    # trips_joined = a list of trips joinee by this user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors["destination"] = "** Destination must be provided and should be at least 3 characters **"
        if len(postData['plan']) < 3:
            errors["plan"] = "** Plan must be provided and should be at least 3 characters **"
        if len(postData['start_date']) == 0:
            errors["start_date_existance"] = "** Start date must be provided **"
        if len(postData['end_date']) == 0:
            errors["end_date_existance"] = "** End date must be provided **"
        
        today = date.today().isoformat()
        if postData['start_date'] < today:
            errors["start_date"] = "** Time travel is not allowed: Start date must be in the future **"
        if postData['end_date'] < postData['start_date']:
            errors["end_date"] = "** End date must be past start date **"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField(max_length=255)
    end_date = models.DateField(max_length=255)
    plan = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="trips_created", on_delete = models.CASCADE)
    users_who_joined = models.ManyToManyField(User, related_name="trips_joined")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()