from django.urls import path
from . import views
urlpatterns=[
  path("contact/",views.contact_view,name="contact"),
  path("",views.index_view,name="index"),
  path("about/",views.about_view,name="about"),
  path("diagnoser/",views.diagnoser_view,name="diagnoser"),
  path("hospitals-nearby/",views.hospitals_nearby_view,name="hospitals-nearby"),
  path("login/",views.login_view,name="login"),
  path("sign_up/",views.sign_up_view,name="sign_up"),
  path("logout/",views.logout_view,name="logout"),
  path("disease/",views.disease_view,name="disease"),
  path("mental/",views.mental_view,name="mental"),
  path('medicine/', views.medicine_list, name='medicine_list'),
  path('search/', views.search_medicine, name='search_medicine'),
  path('medicine/<int:id>/', views.medicine_detail, name='medicine_detail'),   #1 2 3 4 
  path('get-departments/', views.get_departments, name='get_departments'),
  path('get-doctors/', views.get_doctors, name='get_doctors'),
  path('available-times/', views.get_available_times, name='get_available_times'),
  path('heart/', views.heart_predict, name='heart_predict'),
  path('lung/', views.lung_predict, name='lung_predict'),
  path('diabetes/', views.diabetes_predict, name='diabetes_predict'),
  path('stroke/',views.stroke_predict,name='stroke_predict'),
  path('kidney_stone/', views.kidney_stone_predict, name='predict_kidney_stone'),
  path('liver_disease/',views.liver_disease_predict,name='liver_disease_predict'),
  path('prob_display/',views.prob_display,name='display_probability')
] 