from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . models import User
from . models import Recipe
import bcrypt


def index(request):
    return render(request, 'index.html')


def create_user(request):
    errors = User.objects.registration_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

    hash_pw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        username=request.POST["username"],
        password=hash_pw
    )
    request.session['logged_user'] = new_user.id

    return redirect('/dashboard')


def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if request.method == "POST":
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        print("madeitthisfar")
        user = User.objects.filter(email=request.POST['email'])
        print(user)
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['log_user'] = log_user.id
                return redirect('/dashboard')
            else:
                messages.error(request, "Email or Password is incorrect.")
                return redirect('/')

    return redirect('/')

def dashboard(request):
    if "logged_user" not in request.session:
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'all_recipes': Recipe.objects.all()
    }
    return render(request, 'dashboard.html', context)

def create_recipe(request):
    if request.method == "GET":
        return render(request, 'new.html')
    errors = Recipe.objects.recipe_validator(request.POST)
    if request.method == "POST" or request.session['logged_user'] in request.session:
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/recipe/create')
        this_user = User.objects.filter(id=request.session['logged_user'])[0]

        new_recipe = Recipe.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            ingredients=request.POST['ingredients'],
            recipe_content=request.POST['recipe_content'],
            posted_by.set()
        )
        return redirect('/dashboard')
    
def edit_recipe(request, recipe_id):
    if request.method == "GET":
        context = {
            'this_recipe': Recipe.objects.get(id=recipe_id)
        }
        return render(request, 'editrecipe.html', context)


def update_recipe(request, recipe_id):
    errors = Recipe.objects.recipe_validator(request.POST)
    if request.method == "POST" or request.session['logged_user'] in request.session:
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
                print(value)
            return redirect(f"/edit/{recipe_id}")
    if request.method == 'POST':
        this_user = User.objects.filter(id=request.session['logged_user'])[0]

        this_recipe = Recipe.objects.filter(id=recipe_id)[0]
        title=request.POST['title'],
        description=request.POST['description'],
        ingredients=request.POST['ingredients'],
        recipe_content=request.POST['recipe_content'],
        posted_by=this_user

        this_recipe.save()
    return redirect('/dashboard')

def edit_user(request, user_id):
    if request.method == "GET":
        context = {
            'this_user': User.objects.get(id=user_id)
        }
        return render(request, 'edituser.html', context)


def update_user(request, user_id):
    errors = User.objects.user_validator(request.POST)
    if request.method == "POST" or request.session['logged_user'] in request.session:
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
                print(value)
            return redirect(f"/edit/{user_id}")
    if request.method == 'POST':
        this_user = User.objects.filter(id=request.session['logged_user'])[0]

        this_user = User.objects.filter(id=user_id)[0]
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        username=request.POST['username'],
        password=request.POST['password']
        posted_by=this_user

        this_user.save()
    return redirect('/dashboard')

def cancel_recipe(request, recipe_id):
    if request.method != "POST" or "logged_user" not in request.session:
        return redirect('/')
    this_recipe = Recipe.objects.get(id=recipe_id)
    this_recipe.delete()
    return redirect('/dashboard')

def cancel_user(request, user_id):
    if request.method != "POST" or "logged_user" not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=user_id)
    this_user.delete()
    return redirect('/dashboard')

def user_display(request, user_id): #GET request
    if request.method == "POST" or "logged_user" not in request.session:
        return redirect ('/')
    this_user= User.objects.get(id=user_id)
    context={
        'all_user_recipes': this_user.recipe.all(),
        'this_user': this_user
    }
    return render (request, 'userdisplay.html', context)
    
def recipe_display(request,recipe_id):
    if request.method == "POST" or "logged_user" not in request.session:
        return redirect ('/')
    context ={
        'this_recipe': Recipe.objects.get(id=recipe_id),
    }    
    return render (request, "recipedisplay.html", context)