from django.urls import include, path
from rest_framework import routers
from ml_app import views
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'labeledDatas', views.LabeledDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'train/', views.train, name="train"),
    path(r'predict/', views.predict, name="predict"),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
