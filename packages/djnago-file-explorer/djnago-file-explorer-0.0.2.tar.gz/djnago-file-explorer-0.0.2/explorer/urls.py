from django.urls import path

from . import views
from .admin import explorer_admin

urlpatterns = [
    path('admin/', explorer_admin.urls),
    path('', views.Explorer.as_view(), name='explorer-main'),

]
