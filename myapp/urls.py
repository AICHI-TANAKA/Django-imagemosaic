from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    path('inquiry/',views.InquiryView.as_view(),name="inquiry"),
    path('upload/',views.UploadView.as_view(),name="upload"),
]