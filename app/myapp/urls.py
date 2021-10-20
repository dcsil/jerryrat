from django.urls import path
from .views import (
    data_entry_page, 
    campaign_customization_page, 
    analytics_dashboard_page, 
    calling_operations_page, 
    model_controlls_page
)

urlpatterns = [
    path('', data_entry_page, name='data_entry_page'),
    path('data_entry_page/', data_entry_page, name='data_entry_page'),
    path('data_entry_page/', data_entry_page, name='data_entry_page'),
    path('analytics_dashboard_page/', analytics_dashboard_page, name='analytics_dashboard_page'),
    path('calling_operations_page/', calling_operations_page, name='calling_operations_page'),
    path('model_controlls_page/', model_controlls_page, name='model_controlls_page'),
    path('campaign_customization_page/', campaign_customization_page, name='campaign_customization_page'),
]
