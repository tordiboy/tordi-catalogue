
from django.contrib import admin
from django.urls import path, include
from books import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),

    # authentication
    path("accounts/login/", book_views.login_view, name="login"),
    path("accounts/logout/", book_views.logout_view, name="logout"),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)