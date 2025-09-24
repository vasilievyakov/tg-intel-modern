# Deploy script for tg-intel (PowerShell)
param(
    [switch]$Help
)

if ($Help) {
    Write-Host "🚀 tg-intel Deployment Script" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\scripts\deploy.ps1"
    Write-Host ""
    Write-Host "This script will guide you through the deployment process."
    exit 0
}

Write-Host "🚀 Starting deployment process..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Please run this script from the project root" -ForegroundColor Red
    exit 1
}

# Check if git is available
try {
    git --version | Out-Null
} catch {
    Write-Host "❌ git is required but not installed. Aborting." -ForegroundColor Red
    exit 1
}

Write-Host "📋 Deployment checklist:" -ForegroundColor Yellow
Write-Host "1. ✅ Repository is ready"
Write-Host "2. 🔄 Backend will be deployed to Railway"
Write-Host "3. 🔄 Frontend will be deployed to Vercel"
Write-Host "4. 🔄 Database should be configured in Supabase"

Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Push your changes to GitHub:"
Write-Host "   git add ."
Write-Host "   git commit -m 'Prepare for deployment'"
Write-Host "   git push origin main"

Write-Host ""
Write-Host "2. Deploy Backend to Railway:" -ForegroundColor Cyan
Write-Host "   - Go to https://railway.app"
Write-Host "   - Connect your GitHub repository"
Write-Host "   - Create new service from repository"
Write-Host "   - Set environment variables from .env.example"
Write-Host "   - Railway will auto-detect Dockerfile and deploy"

Write-Host ""
Write-Host "3. Deploy Frontend to Vercel:" -ForegroundColor Cyan
Write-Host "   - Go to https://vercel.com"
Write-Host "   - Connect your GitHub repository"
Write-Host "   - Set root directory to 'apps/frontend'"
Write-Host "   - Set NEXT_PUBLIC_API_BASE to your Railway backend URL"
Write-Host "   - Vercel will auto-detect Next.js and deploy"

Write-Host ""
Write-Host "4. Update CORS settings:" -ForegroundColor Cyan
Write-Host "   - After frontend deployment, update CORS_ORIGINS in Railway"
Write-Host "   - Set to your Vercel frontend URL"

Write-Host ""
Write-Host "📚 For detailed instructions, see docs/DEPLOY.md" -ForegroundColor Blue
Write-Host "🎉 Happy deploying!" -ForegroundColor Green
