"""ChaintipStats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from reddit_tips import views as reddit_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', reddit_views.main, name='reddit_main'),
    path('gettips/', reddit_views.populate_db, name='get_reddit_tips'),
    path('export/', reddit_views.export_csv_all_tips, name='export_tips_csv'),

]
