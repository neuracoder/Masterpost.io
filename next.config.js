/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  // Environment variables available to the client
  // env: {
  //   NEXT_PUBLIC_API_URL_PROCESSING: process.env.NEXT_PUBLIC_API_URL_PROCESSING,
  //   NEXT_PUBLIC_API_URL_AUTH: process.env.NEXT_PUBLIC_API_URL_AUTH,
  // },

  // Image configuration
  images: {
    unoptimized: true, // from next.config.mjs
  },

  // Output configuration for production
  output: 'standalone',

  // ESLint and TypeScript configuration from next.config.mjs
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },

  // Rewrites from next.config.mjs
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: 'http://localhost:8002/api/:path*',
  //     },
  //   ]
  // },
}

module.exports = nextConfig
