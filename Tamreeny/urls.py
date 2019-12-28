from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('trainees/', include('trainees.urls'), name='trainees'),
    path('health/', include('health_app.urls'), name='health'),
    path('predict/', include('predictor.urls'), name='predictor'),
    #path('trainers/', include('trainers.urls'), name='trainers'),
    # path('physique_test/', include('physique_test.urls'), name='physique_test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
