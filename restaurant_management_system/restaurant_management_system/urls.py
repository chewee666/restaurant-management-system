from django.contrib import admin
from django.urls import path, include  # 确保导入 path 和 include
from food_menu import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # 设置主页路由
    path('food_menu/', include('food_menu.urls')),  # 包含 food_menu 应用的路由
    path('login/', views.owner_login, name='login'),
    path('logout/', views.owner_logout, name='logout'),
]

# 在开发环境下提供媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
