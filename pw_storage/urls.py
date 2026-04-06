from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home-page"),
    path('register/', views.register_page, name="register-page"),
    path('login/', views.login_page, name="login-page"),
    path('logout/', views.logout_page, name="logout-page"),
    path('passwords/', views.password_list, name="password-list"),
    path('add_password/', views.add_password, name="add-password"),
    path("update/<int:id>/", views.update_password, name="update-password"),
    path("delete/<int:id>/", views.delete_password, name="delete-password"),
    path('passwords/', views.password_list, name='password_list'),

    

]


