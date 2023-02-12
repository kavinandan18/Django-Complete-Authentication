from django.urls import path
from . import views


urlpatterns=[
    path('signup', views.SignupCreateView.as_view(), name= 'signup'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('logout/', views.UserLogOutViews.as_view(), name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/',views.ProfileUpdateView.as_view(),name= 'edit-profile'),
    path('password-reset/',views.Password_Reset_View.as_view(),name= 'password_reset'),
    path('password-reset/done/',views.Password_Reset_Done_View.as_view(),name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/',views.Password_Reset_Confirm_View.as_view(),name= 'password_reset_confirm'),
    path('reset/done/',views.Password_Reset_Complete_View.as_view(),name= 'password_reset_complete'),
    path('password-change/',views.Password_Change_View.as_view(),name= 'password_change'),
    path('password-change/done/',views.Password_Change_Done_Views.as_view(),name= 'password_change_done'),




    
]