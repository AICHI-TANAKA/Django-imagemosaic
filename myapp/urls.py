from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    path('inquiry/',views.InquiryView.as_view(),name="inquiry"),
    path('upload/<int:pk>/',views.UploadView.as_view(),name="upload"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path('my_page/<int:pk>/',views.MyPage.as_view(),name="my_page"),
]