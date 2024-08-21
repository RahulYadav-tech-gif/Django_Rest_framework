from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('', home, name="home"),
    # path('student/', post_student, name="post_student"),
    # path('update-student/<id>/', update_student, name="update_student"),
    # path('delete-student/<id>/', delete_student, name="delete_student"),
    path('', get_book, name="get_book"),
    path('student/', StudentAPI.as_view()),
    path('generic-student/', StudentGeneric.as_view()),
    path('generic-student/<id>', StudentGeneric1.as_view()),
    path('register/', RegisterUser.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pdf/', GeneratePdf.as_view()),
    path('excel/',ExportImportExcel.as_view()),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()