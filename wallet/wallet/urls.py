from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('expenses.urls')),
    # path('authentication/', include('authentication.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),    
    path('income/', include('userincome.urls')),
    path('admin/', admin.site.urls),
]
