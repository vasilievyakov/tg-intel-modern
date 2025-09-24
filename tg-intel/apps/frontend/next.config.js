/** @type {import('next').NextConfig} */
const nextConfig = {
  // Next.js 15 optimizations
  experimental: {
    // Enable React 19 features
    reactCompiler: false, // Disable for now as it's experimental
  },
  // Bundle pages router dependencies for better performance
  bundlePagesRouterDependencies: true,
  // Server external packages
  serverExternalPackages: ['telethon'],
};
module.exports = nextConfig;


