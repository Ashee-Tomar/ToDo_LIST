from unicodedata import name
from django.urls import path
from .views import mark_task, user_logout, welcome_page, add_task, delete_task,user_login, user_signup, user_logout

urlpatterns = [
    path('',welcome_page,name='home_page'),
    # path('view_task/<str:id>', show_task, name='view_task'),
    path('add_task', add_task, name="add_task"),
    path('delete_task/<str:id>', delete_task, name='delete_task'),
    path('mark_task/<str:id>', mark_task, name='mark_task'),
    path('login/', user_login, name='user_login'),
    path('signup/', user_signup, name='user_signup'),
    path('logout/', user_logout, name='user_logout')
]