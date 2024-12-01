""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('login/', views.login_view, name='login'),
    path('vip/',views.vip,name="vip"),
    path('setting/',views.setting,name="setting"),
    path('historique/',views.historique,name="historique"),
    path('deposit/',views.deposit,name="deposit"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('me/',views.me,name="me"),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)