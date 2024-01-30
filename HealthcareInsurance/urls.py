from django.contrib import admin
from django.urls import path, include
from HealthCareInsuranceApp import views

urlpatterns = [
    # path('', include('basicApp.urls')),
    path('prediction/', include('HealthCareInsuranceApp.urls'), name='prediction'),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('admin/', admin.site.urls),
]
