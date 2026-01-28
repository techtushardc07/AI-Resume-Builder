# PowerShell script to set up Git and upload project to GitHub
# Run this script after installing Git

Write-Host "🚀 Setting up Git for AI-powered Learning Assistant project..." -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed! Please install Git first from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# Configure Git (you may want to change these)
$gitName = "Krishna Purwar"
$gitEmail = "krishnarnpur697@gmail.com"  # Replace with your actual email

git config --global user.name $gitName
git config --global user.email $gitEmail
Write-Host "✅ Git configured with name: $gitName, email: $gitEmail" -ForegroundColor Green

# Navigate to project directory
$projectPath = "C:\Users\krish\OneDrive\Desktop\Ai career agent"
Set-Location $projectPath
Write-Host "📁 Working in directory: $projectPath" -ForegroundColor Yellow

# Initialize Git if not already initialized
if (!(Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git repository already exists" -ForegroundColor Blue
}

# Add remote origin
$remoteUrl = "https://github.com/krishnarnpur697-star/Ai-powered-resume-builder.git"
try {
    git remote add origin $remoteUrl
    Write-Host "✅ Remote origin added: $remoteUrl" -ForegroundColor Green
} catch {
    Write-Host "ℹ️  Remote origin might already exist, continuing..." -ForegroundColor Blue
}

# Add all files
git add .
Write-Host "✅ All files added to staging area" -ForegroundColor Green

# Check status
$status = git status --porcelain
if ($status) {
    Write-Host "📋 Files to be committed:" -ForegroundColor Yellow
    Write-Host $status
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Blue
}

# Commit
$commitMessage = "Initial commit: AI-powered Learning Assistant for SDG 4"
git commit -m $commitMessage
Write-Host "✅ Changes committed with message: '$commitMessage'" -ForegroundColor Green

# Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push -u origin main
    Write-Host "🎉 Successfully uploaded to GitHub!" -ForegroundColor Green
    Write-Host "🌐 Repository URL: https://github.com/krishnarnpur697-star/Ai-powered-resume-builder" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Push failed. This might be due to:" -ForegroundColor Red
    Write-Host "   1. Authentication issues (use Personal Access Token)" -ForegroundColor Red
    Write-Host "   2. Repository doesn't exist or you don't have access" -ForegroundColor Red
    Write-Host "   3. Branch name issues (try 'master' instead of 'main')" -ForegroundColor Red
    Write-Host "" -ForegroundColor Red
    Write-Host "Try these solutions:" -ForegroundColor Yellow
    Write-Host "1. Create a Personal Access Token at: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host "2. Use the token as password when prompted" -ForegroundColor Yellow
    Write-Host "3. Or try: git push -u origin master" -ForegroundColor Yellow
}

Write-Host "" -ForegroundColor Green
Write-Host "🎯 Next steps:" -ForegroundColor Green
Write-Host "1. Visit your GitHub repository" -ForegroundColor Green
Write-Host "2. Add a repository description" -ForegroundColor Green
Write-Host "3. Update README.md if needed" -ForegroundColor Green
Write-Host "4. Consider adding GitHub Actions for CI/CD" -ForegroundColor Green

Write-Host "" -ForegroundColor Cyan
Write-Host "Happy coding! 🚀" -ForegroundColor Cyan