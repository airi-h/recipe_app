from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("ホームページです")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls', namespace='recipes')),  # レシピアプリのURLを読み込む
    path('', home, name='home'),  # 仮のホームページ
]

# メディアファイルの提供設定 (DEBUGモードのとき)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
