from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Skill exchange operations
    path('exchange/<int:exchange_id>/accept/', views.accept_exchange, name='accept_exchange'),
    path('exchange/<int:exchange_id>/complete/', views.complete_exchange, name='complete_exchange'),
    path('exchange/<int:exchange_id>/cancel/', views.cancel_exchange, name='cancel_exchange'),
    path('exchange/<int:exchange_id>/delete/', views.delete_exchange, name='delete_exchange'),
    
    # Chat functionality
    path('chat/<int:exchange_id>/', views.chat, name='chat'),
    
    # Review system
    # path('exchange/<int:exchange_id>/review/', views.add_review, name='add_review'),
    
    # API endpoints
    path('api/messages/<int:exchange_id>/', views.get_messages, name='get_messages'),
    path('api/send-message/<int:exchange_id>/', views.send_message, name='send_message'),
]