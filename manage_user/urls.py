from django.urls import path
from . import views

urlpatterns = [
    # path('create_new_project/', views.create_new_project, name='create_new_project'),
		# path('get_all_projects/', views.get_all_projects, name='get_all_projects'),
		path('camera/', views.Home, name='home'),
		# path('get_image/', views.get_image, name='get_image'),
		#  path('stream_video/', views.stream_video, name='stream_video'),
]
