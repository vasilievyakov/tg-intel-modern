#!/bin/bash

# Deploy script for tg-intel
set -e

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the project root"
    exit 1
fi

# Check if required tools are installed
command -v git >/dev/null 2>&1 || { echo "❌ git is required but not installed. Aborting." >&2; exit 1; }

echo "📋 Deployment checklist:"
echo "1. ✅ Repository is ready"
echo "2. 🔄 Backend will be deployed to Railway"
echo "3. 🔄 Frontend will be deployed to Vercel"
echo "4. 🔄 Database should be configured in Supabase"

echo ""
echo "📝 Next steps:"
echo "1. Push your changes to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for deployment'"
echo "   git push origin main"

echo ""
echo "2. Deploy Backend to Railway:"
echo "   - Go to https://railway.app"
echo "   - Connect your GitHub repository"
echo "   - Create new service from repository"
echo "   - Set environment variables from .env.example"
echo "   - Railway will auto-detect Dockerfile and deploy"

echo ""
echo "3. Deploy Frontend to Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Connect your GitHub repository"
echo "   - Set root directory to 'apps/frontend'"
echo "   - Set NEXT_PUBLIC_API_BASE to your Railway backend URL"
echo "   - Vercel will auto-detect Next.js and deploy"

echo ""
echo "4. Update CORS settings:"
echo "   - After frontend deployment, update CORS_ORIGINS in Railway"
echo "   - Set to your Vercel frontend URL"

echo ""
echo "📚 For detailed instructions, see docs/DEPLOY.md"
echo "🎉 Happy deploying!"
