from django.urls import path
from .views import UploadDataView

app_name = 'db'

urlpatterns = [
    path('upload-data/', UploadDataView.as_view(), name='upload-data'),
] 