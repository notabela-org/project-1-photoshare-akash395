from django.urls import path

from feed import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<str:username>', views.profile, name='profile'),
    path('new-post', views.newpost, name='new-post'),
    path('edit-profile', views.editprofile, name='edit-profile'),
    path('post/<int:id>',views.post, name='post'),
]
