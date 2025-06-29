from django.contrib import admin
from django.urls import path, include
from tracker  import views # Make sure this import is correct based on your project structure

urlpatterns = [
    path('admin/', admin.site.urls),
    # Public facing pages
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('repositories/', views.repositories_view, name='repositories'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    path('help/', views.help_view, name='help'),

    # API Endpoints (proxies for GitHub API)
    path('api/get_commits/', views.get_commits_api, name='get_commits_api'),
    path('api/get_repos/', views.get_repos_api, name='get_repos_api'),
    path('api/get_profile/', views.get_github_profile_api, name='get_github_profile_api'), # New API endpoint for profile
    
    # Removed GitHub OAuth related paths
    # path('github_login/', views.github_login_initiate, name='github_login_initiate'),
    # path('github_callback/', views.github_callback, name='github_callback'),
    # path('github_logout/', views.github_logout, name='github_logout'),
]