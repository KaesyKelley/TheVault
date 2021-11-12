from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create_user', views.create_user),
    path('dashboard', views.dashboard),
    path('user/<int:user_id>recipe', views.user_display),
    path('user/login', views.login),
    path('recipe/create', views.create_recipe),
    #path('create', views.create_recipe),
    path('edit/<int:user_id>', views.edit_user),
    path('edit/<int:recipe_id>', views.edit_recipe),
    path('<int:recipe_id>/cancel', views.cancel_recipe),
    path('logout', views.index),
    path('update/<int:recipe_id>', views.update_recipe),
    path('update/<int:user_id>', views.update_user),
    #path('granted/<int:recipe_id>', views.granted)
    path('<int:recipe_id>', views.recipe_display),
    path('edituser', views.edit_user)
]