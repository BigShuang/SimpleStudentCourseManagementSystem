from django.urls import path
from user import views

urlpatterns = [
    path('views/', views.home, name="views"),
    path('views/<slug:kind>', views.login, name="views"),
    path('register/<slug:kind>', views.register, name="register"),

    path('update/<slug:kind>', views.update, name="update"),
    path('logout/', views.logout, name="logout"),
]
