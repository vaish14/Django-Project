from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'index/', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'courses/',views.courses, name='courses'),
    path(r'<int:course_no>/add_interest/', views.add_interest, name='add_interest'),
    path(r'courses/<int:course_no>/', views.coursedetail, name='coursedetail'),
    path(r'placeorder', views.placeorder, name='placeorder'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myaccount/', views.myaccount, name='myaccount')
]
