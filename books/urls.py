from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post_book, name='post_book'),
    path('chat/', views.chat_view, name='chat'),
    path('about/', views.about_us, name='about_us'),
    path('books/', views.book_list, name='book_list'),
    path('send_message/', views.send_message, name='send_message'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('download/<int:book_id>/', views.download_book, name='download_book'),
]