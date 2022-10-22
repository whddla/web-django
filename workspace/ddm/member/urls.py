from django.urls import path
from . import views


urlpatterns = [
    path('agreements/', views.agreements),
    path('join/', views.join),
    path('join/idduplicate', views.idDuplicateCheck),
    path('join/nickduplicate', views.nickDuplicateCheck),
    path('join/phnumduplicate', views.phnumDuplicateCheck),
    path('join/selfPhoneCheck', views.selfPhoneCheck),
    path('join/create', views.createMember),
    path('login/', views.login),
    path('login/result', views.checkLogin),
    path('logout/', views.logout),
    path('mypage/', views.mypage_sellProducts),
    path('mypage/buyproducts', views.mypage_buyProducts),
    path('mypage/reviews', views.mypage_reviews),
    path('mypage/wishes', views.mypage_wishList),
    path('mypage/qna', views.one_on_one),
    path('mypage/alarm', views.mypage_alarm),
    path('mypage/alarmset', views.mypage_alarmSet),
    path('mypage/update', views.mypage_update),
    path('mypage/updateform', views.mypage_updateForm),
    path('mypage/updatemember', views.mypage_updateMember),
    path('mypage/nickduplicate', views.nickDuplicateCheck),
    path('mypage/phnumduplicate', views.phnumDuplicateCheck),
    path('mypage/selfPhoneCheck', views.selfPhoneCheck),
    path('mypage/qna', views.one_on_one),
    path('profile/', views.profile_products),
    path('profile/reviews', views.profile_reviews),
    path('profile/manner', views.profile_manner),
    path('out/', views.memberout),
]
