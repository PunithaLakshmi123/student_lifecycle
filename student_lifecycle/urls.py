from django.contrib import admin
from django.urls import path, include
from students.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),
    # Public landing page
    path('', HomeView.as_view(), name='home'),
    path('', include(('students.web_urls', 'students'), namespace='students')),
]
