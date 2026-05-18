from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('register/', views.register_view, name='register'),

    # 🔐 CUSTOM ADMIN PANEL
    path('admin-unlock/', views.admin_unlock_page, name='admin_unlock'),

    # 🔁 TOGGLE ACCESS (LOCK/UNLOCK)
    path('toggle-access/<int:user_id>/<int:book_id>/',
         views.toggle_book_access,
         name='toggle_access'),
]