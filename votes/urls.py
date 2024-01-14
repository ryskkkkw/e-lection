from django.urls import path

from . import views


app_name = 'votes'
urlpatterns = [
  path('index/', views.IndexView.as_view(),
       name='index'),
  path('select/', views.SelectView.as_view(),
       name='select'),
  path('confirm/', views.ConfirmView.as_view(),
       name='confirm'),
  path('vote/<str:party>/<str:age>/<str:gender>/', 
       views.VoteView.as_view(), name='vote'),
  path('plot/dayly/', views.get_svg_dayly, name='plot_day'),
  path('plot/monthly/', views.get_svg_monthly, name='plot_month'),
  path('plot/transition/', views.get_svg_transition, name='plot_trans'),
]