"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Account
    path('admin/', admin.site.urls),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('account/', views.AccountUpdateView.as_view()),
    #path('profile/', views.ProfileUpdateView.as_view()),

    # Order
    path('orders/<str:pk>/', views.OrderDetailView.as_view()),
    path('orders/', views.OrderIndexView.as_view()),


    # Bookmark
    path('bookmark/add/<str:pk>/', views.BookmarkAddView.as_view(), name='bookmark_add'),
    path('bookmark/delete/<str:pk>/', views.BookmarkDeleteView.as_view(),name='bookmark_delete'),
    #path('bookmark/', views.BookmarkListView.as_view(), name='bookmark_list'),

    # Items
    path('items/<str:pk>', views.ItemDetailView.as_view(), name="item_detail"),
    path('categories/<str:pk>/', views.CategoryListView.as_view()),
    path('tags/<str:pk>/', views.TagListView.as_view()),
    path('new/', views.ItemCreateView.as_view(), name="new"),
    path('edit/<str:pk>/', views.ItemUpdateView.as_view(), name="edit"),

    path('', views.IndexListView.as_view(), name="list"),
    path('bookmark/', views.BookmarkListView.as_view(), name='bookmark'),  


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
