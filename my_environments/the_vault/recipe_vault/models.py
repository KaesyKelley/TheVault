from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) > 45:
            errors["first_name"] = "First Name should be no more than 45 characters"
        if len(postData['last_name']) >= 45:
            errors["last_name"] = "Last Name should be no more than 45 characters"
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        users_email = User.objects.filter(email = postData['email'])
        if len(users_email) >= 1:
            errors["copy"] = "Email address is already in system, please try again."
        if len(postData['username']) > 45:
            errors["username"] = "UserName should be no more than 45 characters"
        if len(postData['password']) < 5:
            errors["password"] = "Password must be at least 5 characters"
        if postData['password'] != postData['password_confirmation']:
            errors["pw_match"] = "Passwords must match"
        return errors
    def login_validator(self, postData):
        errors ={}
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        users_email = User.objects.filter(email = postData['email'])
        if len(users_email) == 0:
            errors["invalid"] = "Email or password is invalid, please try again."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #relatedname thisUser
    
class RecipeManager(models.Manager):
    def recipe_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "A Title must consist of at least 3 characters!"
        if len(postData['description']) < 10:
            errors["description"] = "A description must be more than 10 characters!"
        if len(postData['ingredients']) < 10:
            errors["ingredients"] = "Ingredients list must contain more than 10 characters!"
        if len(postData['recipe_content']) < 10:
            errors["recipe_content"] = "A recipe must be more than 10 characters!"
        return errors

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    recipe_content = models.TextField()
    posted_by = models.ManyToManyField(User, related_name="thisuser")
    #MTM
    date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    granted = models.BooleanField(default=False)
    objects = RecipeManager()


