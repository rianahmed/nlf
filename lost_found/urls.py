from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('admin_volt.urls')),
    path('admin/', admin.site.urls),
    path('lost-item-report/', include('lost_item_report.urls')),
]