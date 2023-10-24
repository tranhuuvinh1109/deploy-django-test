from django.urls import path
from . import views

urlpatterns = [
    path('create_new_project/', views.create_new_project, name='create_new_project'),
		path('get_all_projects/', views.get_all_projects, name='get_all_projects'),
		path('camera/<str:name>/', views.video_stream, name='video_stream'),
]
