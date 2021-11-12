from django.urls import path, include

urlpatterns = [
    path('', include('recipe_vault.urls')),
]
