# JioCX Performance Predictor Git Initialization Script

Write-Host "=========================================" -ForegroundColor Green
Write-Host "🚀 JioCX Performance Predictor Git Setup" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Git is not installed on this system. Please download and install Git from https://git-scm.com/ before running this script."
    Read-Host "Press Enter to exit..."
    exit
}

# Check if repo is already initialized
if (Test-Path .git) {
    Write-Host "ℹ️ Git repository is already initialized in this folder." -ForegroundColor Yellow
} else {
    Write-Host "📦 Initializing local Git repository..." -ForegroundColor Cyan
    git init
}

# Add all files (respecting .gitignore)
Write-Host "📂 Staging project files..." -ForegroundColor Cyan
git add .

# Initial Commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit - JioCX Performance Predictor & Success Profile Analysis"

# Set branch name to main
git branch -M main

Write-Host ""
Write-Host "🎉 Local repository initialized and committed successfully!" -ForegroundColor Green
Write-Host ""

# Ask for Remote URL
$remoteUrl = Read-Host "🔗 Enter your GitHub / GitLab remote repository URL (leave blank to skip pushing now)"
if ($remoteUrl) {
    # Check if origin already exists
    $existingRemote = git remote
    if ($existingRemote -contains "origin") {
        Write-Host "Replacing existing remote 'origin'..." -ForegroundColor Yellow
        git remote remove origin
    }
    git remote add origin $remoteUrl
    Write-Host "📤 Pushing project to remote repository..." -ForegroundColor Cyan
    git push -u origin main
    Write-Host "🚀 Project pushed successfully!" -ForegroundColor Green
} else {
    Write-Host "⏩ Skipped remote configuration. You can connect it later using: git remote add origin <URL>" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit..."
