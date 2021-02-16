
from django.urls import path
from . import views



urlpatterns=[
    path('',views.index,name="page1"),
    
    path('home',views.index,name="page1"),


    path('User_Reg',views.input,name="registration"),
    path('User_input',views.testinput,name="testinput"),
    path('user_test',views.veri,name="test_page"),
    path('input',views.reg,name="name"),
    path('start_test1',views.startproc,name="test start"),
    path('submit',views.stop,name="bdb")
]