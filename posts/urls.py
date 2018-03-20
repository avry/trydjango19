from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [

	path('', views.post_list, name = 'list'),
	path('create/', views.post_create),
	path('<int:id>/', views.post_detail, name = 'detail'),
	path('<int:id>/edit', views.post_update, name = 'update'),
	path('delete/<int:id>', views.post_delete),

]