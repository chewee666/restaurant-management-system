from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_food, name='add_food'),
    path('menu/', views.food_menu, name='food_menu'),
    path('list/', views.food_list, name='food_list'),
    path('edit/<int:food_id>/', views.edit_food, name='edit_food'),
    path('hide/<int:food_id>/', views.hide_food, name='hide_food'),
    path('login/', views.owner_login, name='owner_login'),
    path('logout/', views.owner_logout, name='owner_logout'),
    path('bulk_delete/', views.bulk_delete, name='bulk_delete'),  # 批量删除路由
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('temporary_file/', views.temporary_file, name='temporary_file'),  # 查看临时文件的路由
    path('restore/<int:food_id>/', views.restore_food, name='restore_food'),  # 恢复食物的路由
    path('delete_permanently/<int:food_id>/', views.delete_food_permanently, name='delete_food_permanently'),
    # 永久删除食物的路由
]
