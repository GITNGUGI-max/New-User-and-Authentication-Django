from .  import views
from django.urls import path



urlpatterns = [
    path('',  views.PostList.as_view(), name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('register', views.register_request, name='register'),

]