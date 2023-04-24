from django.contrib import admin
from django.urls import path
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', views.account_list),
    path('account/<int:id>', views.account_info),
    path('dest/', views.dest_list),
    path('server/incoming_data/', views.data_handler),
]