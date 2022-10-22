from django.urls import path
from . import views

urlpatterns = [
    path('buy/',views.buy),
    path('manage/',views.manage),
    path('new/',views.new),
    path('detail/',views.detail),
    # path('new/main/',views.new_main),
    path('upload/',views.fileUpload1),
    path('delete/<int:idx>', views.remove, name='delete'),
    path('update/<int:idx>', views.update, name='update'),
    path('sell/',views.sell),
    path('heart/',views.heart),             # Ajax 찜 버튼 호출
    path('purchase/',views.purchase),       # Ajax 구매 버튼 호출
]


