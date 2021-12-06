from django.urls import path
from .views import *

# for the purpose of testing page integrity
page_names = ['data_entry_page',
              'analytics_dashboard_page',
              'calling_operations_page',
              'model_controlls_page',
              'campaign_customization_page']

urlpatterns = [
    path('', LogIn.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    
    path('data_entry_page/', data_entry_page, name='data_entry_page'),
    path('data_entry_page/', data_entry_page, name='data_entry_page'),
    path('analytics_dashboard_page/', analytics_dashboard_page, name='analytics_dashboard_page'),
    path('delete_graph/<int:id>/', delete_graph, name='delete_graph'),
    path('configure_graph/<int:id>/', configure_graph, name='configure_graph'),
    path('calling_operations_page/', calling_operations_page, name='calling_operations_page'),
    path('model_controlls_page/', model_controlls_page, name='model_controlls_page'),
    path('campaign_customization_page/', campaign_customization_page, name='campaign_customization_page'),
]
