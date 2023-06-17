from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('underlying/', views.underlying, name='underlying-page'),
    path('option/', views.option, name='option-page'),
    path('underlying/make_underlying', views.make_underlying, name='make_underlying'),
    path('underlying/clear_underlying_dictionary', views.clear_underlying_dictionary, name='clear_underlying_dictionary'),
    path('option/make_option', views.make_option, name='make_option'),
    path('option/clear_option_dictionary', views.clear_option_dictionary, name='clear_option_dictionary'),
    path('home/make_price', views.make_price, name='make_price'),
    path('home/clear_price_dictionary', views.clear_price_dictionary, name='clear_price_dictionary'),

]

