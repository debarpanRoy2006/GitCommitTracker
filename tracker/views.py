import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
# from django.contrib.auth import login as auth_login, logout as auth_logout # No longer needed for this model
# from django.contrib.auth.models import User # No longer directly managing Django Users for GitHub data

# --- Views for serving HTML pages ---

def home_view(request):
    """Renders the home page."""
    return render(request, 'home.html')

def dashboard_view(request):
    """Renders the dashboard page (index.html)."""
    return render(request, 'index.html')

def profile_view(request):
    """
    Renders the profile page. It will now fetch profile data based on
    a username provided via frontend JavaScript, not from Django session login.
    """
    return render(request, 'profile.html')

def repositories_view(request):
    """Renders the repositories page."""
    return render(request, 'repositories.html')

def settings_view(request):
    """Renders the settings page."""
    return render(request, 'settings.html')

def about_view(request):
    """Renders the about page."""
    return render(request, 'about.html')

def help_view(request):
    """Renders the help page."""
    return render(request, 'help.html')


# --- GitHub API Proxy/Helper View for Commits ---

def get_commits_api(request):
    """
    API endpoint to fetch commits for a given GitHub repository.
    This is typically called by your frontend JavaScript.
    """
    username = request.GET.get("username")
    repo = request.GET.get("repo")
    branch = request.GET.get("branch", "main")
    since = request.GET.get('since')
    until = request.GET.get('until')

    if not username or not repo:
        return JsonResponse({"error": "Username and repository are required."}, status=400)

    url = f"https://api.github.com/repos/{username}/{repo}/commits?sha={branch}"
    if since:
        url += f"&since={since}T00:00:00Z"
    if until:
        url += f"&until={until}T23:59:59Z"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        # WARNING: Without a token (authentication), GitHub's API rate limit is very low (60 requests/hour per IP).
        # "Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}" if hasattr(settings, 'GITHUB_PERSONAL_ACCESS_TOKEN') else None,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        commits_data = response.json()

        processed_commits = []
        for commit_item in commits_data:
            author_name = commit_item['commit']['author']['name'] if commit_item.get('commit') and commit_item['commit'].get('author') else 'Unknown'
            commit_date = commit_item['commit']['author']['date'][:10] if commit_item.get('commit') and commit_item['commit'].get('author') else ''
            avatar_url = commit_item['author']['avatar_url'] if commit_item.get('author') else 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'

            processed_commits.append({
                'message': commit_item['commit']['message'],
                'author': author_name,
                'date': commit_date,
                'avatar_url': avatar_url,
                'html_url': commit_item['html_url'],
            })
        return JsonResponse({'commits': processed_commits})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching commits from GitHub API: {e}")
        error_message = f"Failed to fetch commits: {e}"
        if 'response' in locals() and response.status_code == 403:
            error_message = "GitHub API rate limit exceeded or access forbidden. Please try again later."
        elif 'response' in locals() and response.status_code == 404:
            error_message = f"Repository '{username}/{repo}' not found or does not exist."
        return JsonResponse({"error": error_message, "status_code": response.status_code if 'response' in locals() else 500}, status=500)


# --- GitHub API Proxy/Helper View for Repositories ---

def get_repos_api(request):
    """
    API endpoint to fetch public repositories for a given GitHub username.
    This is called by your frontend JavaScript on repositories.html.
    """
    username = request.GET.get("username")

    if not username:
        return JsonResponse({"error": "Username is required."}, status=400)

    url = f"https://api.github.com/users/{username}/repos?type=public"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # WARNING: Without a token (authentication), GitHub's API rate limit is very low (60 requests/hour per IP).
        # "Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}" if hasattr(settings, 'GITHUB_PERSONAL_ACCESS_TOKEN') else None,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        repos_data = response.json()

        processed_repos = []
        for repo_item in repos_data:
            processed_repos.append({
                'name': repo_item['name'],
                'html_url': repo_item['html_url'],
                'description': repo_item['description'],
                'stargazers_count': repo_item['stargazers_count'],
                'forks_count': repo_item['forks_count'],
                'language': repo_item['language'],
            })
        return JsonResponse({'repos': processed_repos})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories from GitHub API: {e}")
        error_message = f"Failed to fetch repositories: {e}"
        if 'response' in locals() and response.status_code == 404:
            error_message = f"User '{username}' not found on GitHub."
        elif 'response' in locals() and response.status_code == 403:
            error_message = "GitHub API rate limit exceeded or access forbidden. Please try again later."
        return JsonResponse({"error": error_message, "status_code": response.status_code if 'response' in locals() else 500}, status=500)


# --- NEW: GitHub API Proxy/Helper View for User Profile ---

def get_github_profile_api(request):
    """
    API endpoint to fetch a public GitHub user profile.
    This is called by your frontend JavaScript on profile.html.
    """
    username = request.GET.get("username")

    if not username:
        return JsonResponse({"error": "Username is required."}, status=400)

    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # WARNING: Without a token (authentication), GitHub's API rate limit is very low (60 requests/hour per IP).
        # "Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}" if hasattr(settings, 'GITHUB_PERSONAL_ACCESS_TOKEN') else None,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        profile_data = response.json()

        # Extract only relevant public data
        processed_profile = {
            'login': profile_data.get('login'),
            'name': profile_data.get('name'),
            'avatar_url': profile_data.get('avatar_url'),
            'html_url': profile_data.get('html_url'),
            'bio': profile_data.get('bio'),
            'location': profile_data.get('location'),
            'blog': profile_data.get('blog'),
            'followers': profile_data.get('followers'),
            'following': profile_data.get('following'),
            'public_repos': profile_data.get('public_repos'),
            'created_at': profile_data.get('created_at'),
            'company': profile_data.get('company'),
            'twitter_username': profile_data.get('twitter_username')
        }
        return JsonResponse({'profile': processed_profile})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile from GitHub API: {e}")
        error_message = f"Failed to fetch profile: {e}"
        if 'response' in locals() and response.status_code == 404:
            error_message = f"User '{username}' not found on GitHub."
        elif 'response' in locals() and response.status_code == 403:
            error_message = "GitHub API rate limit exceeded or access forbidden. Please try again later."
        return JsonResponse({"error": error_message, "status_code": response.status_code if 'response' in locals() else 500}, status=500)
