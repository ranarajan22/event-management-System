from django.urls import path
from .views import event_register, event_registrations, signup_view, login_view, logout_view, dashboard_view, event_list, event_create, event_update, event_delete, home, event_detail,index,land,events



urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('events/', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/update/<int:pk>/', event_update, name='event_update'),
    path('events/delete/<int:pk>/', event_delete, name='event_delete'),
    path('detail/<int:pk>/', event_detail, name='event_detail'),
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('events/register/<int:event_id>/', event_register, name='event_register'),
    path('events/registrations/<int:event_id>/', event_registrations, name='event_registrations'),
    path('', land, name='land'),
    path('events/', events, name='events'),
    
]


