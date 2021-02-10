from django.urls import path

from booking import views

urlpatterns = [
    path('vacate/', views.VacateApi.as_view()),
    path('occupy/', views.OccupyApi.as_view()),
    path('get_info/<str:key>', views.GetInfoApi.as_view()),
    path('add_seat', views.AddSeatApi.as_view())
]
