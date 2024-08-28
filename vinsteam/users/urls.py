from django.urls import path
from users.views import (AddressDeleteView, AddressEditView, AddressFormView,
                         CustomLogoutView, PasswordChangeView, UserDetailsView,
                         login_view, register)

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', UserDetailsView.as_view(), name='profile'),
    path(
        'password_change/',
        PasswordChangeView.as_view(),
        name='password_change'),
    path('add_address/', AddressFormView.as_view(), name='add_address'),
    path(
        'address/edit/<int:pk>/',
        AddressEditView.as_view(),
        name='edit_address'),
    path(
        'address/delete/<int:pk>/',
        AddressDeleteView.as_view(),
        name='delete_address'),

]
