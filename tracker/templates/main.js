// DOM Elements
const sidebar = document.getElementById('sidebar');
const content = document.getElementById('content');
const sidebarToggle = document.getElementById('sidebarToggle');

// Navigation links
const homeLink = document.getElementById('homeLink');
const dashboardLink = document.getElementById('dashboardLink');
const profileLink = document.getElementById('profileLink');
const repositoriesLink = document.getElementById('repositoriesLink');
const settingsLink = document.getElementById('settingsLink');
const helpLink = document.getElementById('helpLink');
const aboutLink = document.getElementById('aboutLink');

// Content sections
const homeContent = document.getElementById('homeContent');
const dashboardContent = document.getElementById('dashboardContent');
const profileContent = document.getElementById('profileContent');
const repositoriesContent = document.getElementById('repositoriesContent');
const settingsContent = document.getElementById('settingsContent');
const helpContent = document.getElementById('helpContent');
const aboutContent = document.getElementById('aboutContent');

// Form elements
const commitForm = document.getElementById('commitForm');
const commitList = document.getElementById('commitList');
const loading = document.getElementById('loading');
const settingsForm = document.getElementById('settingsForm');
const settingsStatus = document.getElementById('settingsStatus');

// Toggle sidebar
sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    content.classList.toggle('expanded');
});

// Navigation functions
function clearActiveLinks() {
    [homeLink, dashboardLink, profileLink, repositoriesLink, settingsLink, helpLink, aboutLink].forEach(link => {
    link.classList.remove('active');
    });
}

function hideAllContent() {
    [homeContent, dashboardContent, profileContent, repositoriesContent, settingsContent, helpContent, aboutContent].forEach(section => {
    section.style.display = 'none';
    });
}

function showPage(contentDiv, link) {
    hideAllContent();
    contentDiv.style.display = 'block';
    clearActiveLinks();
    link.classList.add('active');
    
    // If showing profile or repositories, load data if username is available
    const username = document.getElementById('username').value.trim();
    if (contentDiv === profileContent && username) {
    loadProfile(username);
    } else if (contentDiv === repositoriesContent && username) {
    loadRepositories(username);
    }
}

// Event listeners for navigation
homeLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(homeContent, homeLink);
});

dashboardLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(dashboardContent, dashboardLink);
});

profileLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(profileContent, profileLink);
});

repositoriesLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(repositoriesContent, repositoriesLink);
});

settingsLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(settingsContent, settingsLink);
    loadSettings();
});

helpLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(helpContent, helpLink);
});

aboutLink.addEventListener('click', e => {
    e.preventDefault();
    showPage(aboutContent, aboutLink);
});

// Load user profile
function loadProfile(username) {
    const profileInfo = document.getElementById('profileInfo');

    if (!username) {
    profileInfo.innerHTML = `<p class="text-danger">Please enter a GitHub username in the Dashboard first.</p>`;
    return;
    }

    profileInfo.innerHTML = 'Loading profile...';

    fetch(`https://api.github.com/users/${username}`)
    .then(res => {
        if (!res.ok) throw new Error('User not found');
        return res.json();
    })
    .then(user => {
        profileInfo.innerHTML = `
        <img src="${user.avatar_url}" alt="Avatar" class="profile-avatar mb-3" />
        <h3>${user.name || user.login}</h3>
        <p>${user.bio || 'No bio available'}</p>
        <p><strong>Location:</strong> ${user.location || 'Not specified'}</p>
        <p><strong>Public Repositories:</strong> ${user.public_repos}</p>
        <p><strong>Followers:</strong> ${user.followers}</p>
        <p><a href="${user.html_url}" target="_blank" rel="noopener" class="btn btn-primary">View on GitHub</a></p>
        `;
    })
    .catch(err => {
        profileInfo.innerHTML = `<p class="text-danger">Error loading profile: ${err.message}</p>`;
    });
}

// Load repositories
function loadRepositories(username) {
    const repoListDiv = document.getElementById('repoList');

    if (!username) {
    repoListDiv.innerHTML = `<p class="text-danger">Please enter a GitHub username in the Dashboard first.</p>`;
    return;
    }

    repoListDiv.innerHTML = 'Loading repositories...';

    fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=50`)
    .then(res => {
        if (!res.ok) throw new Error('Failed to fetch repositories');
        return res.json();
    })
    .then(repos => {
        if (repos.length === 0) {
        repoListDiv.innerHTML = '<p>No repositories found for this user.</p>';
        return;
        }

        const listHTML = repos.map(repo => `
        <div class="card mb-3">
            <div class="card-body">
            <h5 class="card-title">
                <a href="${repo.html_url}" target="_blank" rel="noopener">${repo.name}</a>
                ${repo.fork ? '<span class="badge bg-secondary ms-2">Fork</span>' : ''}
            </h5>
            <p class="card-text">${repo.description || 'No description'}</p>
            <p class="card-text">
                <small class="text-muted">
                <span class="me-3">⭐ ${repo.stargazers_count}</span>
                <span class="me-3">👁️ ${repo.watchers_count}</span>
                <span>${repo.language || 'Unknown language'}</span>
                </small>
            </p>
            <a href="#" onclick="fetchCommits('${username}', '${repo.name}'); return false;" class="btn btn-sm btn-outline-primary">View Commits</a>
            </div>
        </div>
        `).join('');

        repoListDiv.innerHTML = listHTML;
    })
    .catch(err => {
        repoListDiv.innerHTML = `<p class="text-danger">Error: ${err.message}</p>`;
    });
}

// Fetch commits from GitHub API
function fetchCommits(username, repo, branch = 'main', since = '', until = '') {
    loading.style.display = 'block';
    commitList.innerHTML = '';
    
    let url = `https://api.github.com/repos/${username}/${repo}/commits?sha=${branch}`;
    if (since) url += `&since=${since}`;
    if (until) url += `&until=${until}`;
    
    fetch(url)
    .then(res => {
        if (!res.ok) throw new Error('Failed to fetch commits');
        return res.json();
    })
    .then(commits => {
        loading.style.display = 'none';
        if (commits.length === 0) {
        commitList.innerHTML = '<li class="list-group-item">No commits found for the selected criteria.</li>';
        return;
        }
        
        // Show dashboard with commits
        showPage(dashboardContent, dashboardLink);
        document.getElementById('username').value = username;
        document.getElementById('repo').value = repo;
        document.getElementById('branch').value = branch;
        
        // Display commits
        renderCommits(commits);
    })
    .catch(err => {
        loading.style.display = 'none';
        commitList.innerHTML = `<li class="list-group-item text-danger">Error: ${err.message}</li>`;
    });
}

// Render commits to the page
function renderCommits(commits) {
    commitList.innerHTML = '';
    
    commits.forEach(commit => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex align-items-center commit-item';
    
    const img = document.createElement('img');
    img.src = commit.author?.avatar_url || 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png';
    img.alt = commit.commit.author.name;
    img.className = 'avatar me-3';
    
    const text = document.createElement('div');
    text.innerHTML = `
        <strong>${commit.commit.message.split('\n')[0]}</strong><br/>
        <small>${commit.commit.author.name} - ${new Date(commit.commit.author.date).toLocaleString()}</small>
        <a href="${commit.html_url}" target="_blank" rel="noopener" class="btn btn-sm btn-outline-secondary ms-3">View on GitHub</a>
    `;
    
    li.appendChild(img);
    li.appendChild(text);
    commitList.appendChild(li);
    });
}

// Handle commit form submission
commitForm.addEventListener('submit', e => {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const repo = document.getElementById('repo').value.trim();
    const branch = document.getElementById('branch').value.trim() || 'main';
    const since = document.getElementById('since').value;
    const until = document.getElementById('until').value;
    
    if (!username || !repo) {
    alert('Please enter both username and repository name');
    return;
    }
    
    fetchCommits(username, repo, branch, since, until);
});

// Settings functionality
function loadSettings() {
    const theme = localStorage.getItem('theme') || 'light';
    const defaultBranch = localStorage.getItem('defaultBranch') || 'main';
    
    document.getElementById('themeSelect').value = theme;
    document.getElementById('defaultBranch').value = defaultBranch;
    applyTheme(theme);
}

function applyTheme(theme) {
    if (theme === 'dark') {
    document.body.classList.add('bg-dark', 'text-light');
    document.body.classList.remove('bg-light', 'text-dark');
    document.getElementById('content').classList.add('bg-dark');
    document.getElementById('content').classList.remove('bg-white');
    } else {
    document.body.classList.remove('bg-dark', 'text-light');
    document.body.classList.add('bg-light', 'text-dark');
    document.getElementById('content').classList.remove('bg-dark');
    document.getElementById('content').classList.add('bg-white');
    }
}

settingsForm.addEventListener('submit', e => {
    e.preventDefault();
    
    const theme = document.getElementById('themeSelect').value;
    const defaultBranch = document.getElementById('defaultBranch').value.trim() || 'main';
    
    localStorage.setItem('theme', theme);
    localStorage.setItem('defaultBranch', defaultBranch);
    
    applyTheme(theme);
    
    settingsStatus.style.display = 'inline';
    setTimeout(() => {
    settingsStatus.style.display = 'none';
    }, 2000);
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Show home page by default
    showPage(homeContent, homeLink);
    
    // Load any saved settings
    loadSettings();
});
homeLink.addEventListener('click', e => {
e.preventDefault();
showPage(homeContent, homeLink);

// Collapse sidebar when Home is shown
sidebar.classList.add('collapsed');
content.classList.add('expanded');
});
window.addEventListener('DOMContentLoaded', () => {
showPage(homeContent, homeLink); // Show Home tab
sidebar.classList.add('collapsed'); // Sidebar collapsed by default
content.classList.add('expanded');
});
dashboardLink.addEventListener('click', e => {
e.preventDefault();
showPage(dashboardContent, dashboardLink);

// Expand sidebar on other tabs
sidebar.classList.remove('collapsed');
content.classList.remove('expanded');
});

profileLink.addEventListener('click', e => {
e.preventDefault();
showPage(profileContent, profileLink);

// Expand sidebar on other tabs
sidebar.classList.remove('collapsed');
content.classList.remove('expanded');
});

repositoriesLink.addEventListener('click', e => {
e.preventDefault();
showPage(repositoriesContent, repositoriesLink);

// Expand sidebar on other tabs
sidebar.classList.remove('collapsed');
content.classList.remove('expanded');
});

settingsLink.addEventListener('click', e => {
e.preventDefault();
showPage(settingsContent, settingsLink);

// Expand sidebar on other tabs
sidebar.classList.remove('collapsed');
content.classList.remove('expanded');
});

helpLink.addEventListener('click', e => {
e.preventDefault();
showPage(helpContent, helpLink);

// Expand sidebar on other tabs
sidebar.classList.remove('collapsed');
content.classList.remove('expanded');
});

aboutLink.addEventListener('click', e => {
e.preventDefault();
showPage(aboutContent, aboutLink);

// Expand sidebar on other tabs
sidebar.classList.remove('collapsed');
content.classList.remove('expanded');
});
