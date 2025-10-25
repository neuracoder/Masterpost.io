/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  // Environment variables available to the client
  env: {
    NEXT_PUBLIC_API_URL_PROCESSING: process.env.NEXT_PUBLIC_API_URL_PROCESSING,
    NEXT_PUBLIC_API_URL_AUTH: process.env.NEXT_PUBLIC_API_URL_AUTH,
  },

  // Optimize images
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
  },

  // Output configuration for production
  output: 'standalone',
}

module.exports = nextConfig
