from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path('',views.index),
    path('introduce_company/',views.introduce),
    path('consumer/',views.consumer),
    path('question/',views.question),
    path('upload/',views.fileUpload),
    path('change/<int:no>', views.fileChange, name='fileChange'),
    path('delete/<int:no>', views.fileDelete, name='fileDelete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
