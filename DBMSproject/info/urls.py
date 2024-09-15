from django.urls import path
from . import views

urlpatterns=[
    path('flight details/<str:user>',views.flightDetails,name='flightDetails'),
    path('flight details/details/<flight_no>',views.details,name='details'),
    path('flight details/insert member/',views.insertcabincrew,name='insertcabincrew'),
    path('flight details/insert employee/',views.insertemp,name='insertemp'),
    path('flight details/insertcrew/',views.insertcrew,name='insertcrew'),
    path('flight details/insertgrdemp/',views.insertgrdemp,name='insertgrdemp'),
]