from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import index, CoinListView

urlpatterns = [
    path('', index, name='index'),
    path('api/coins/', CoinListView.as_view(), name='coin-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)