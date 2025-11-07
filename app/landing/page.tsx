"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Check,
  ArrowRight,
  Sparkles,
  Zap,
  Shield,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Star,
} from "lucide-react"

import GalleryShowcase from "@/components/GalleryShowcase"

// Gallery items configuration
const GALLERY_ITEMS = [
  { id: "bicicleta", title: "Complex Vintage Bicycle", description: "Multiple angles & spokes", time: "6s" },
  { id: "lampara", title: "Glass & Metal Lamp", description: "Transparent glass", time: "5s" },
  { id: "joyeria", title: "Jewelry with Reflections", description: "Fine details & shine", time: "4s" },
  { id: "botella", title: "Glass Bottle", description: "Transparency & reflections", time: "5s" },
  { id: "zapato", title: "Leather Shoe", description: "Textures & details", time: "4s" },
  { id: "peluche", title: "Plush Toy", description: "Fuzzy edges", time: "5s" },
]

export default function LandingPage() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [isAutoPlaying, setIsAutoPlaying] = useState(true)
  const [openFaq, setOpenFaq] = useState<number | null>(null)

  // Auto-advance slider
  useEffect(() => {
    if (!isAutoPlaying) return

    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % GALLERY_ITEMS.length)
    }, 5000)

    return () => clearInterval(interval)
  }, [isAutoPlaying])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % GALLERY_ITEMS.length)
    setIsAutoPlaying(false)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + GALLERY_ITEMS.length) % GALLERY_ITEMS.length)
    setIsAutoPlaying(false)
  }

  const goToSlide = (index: number) => {
    setCurrentSlide(index)
    setIsAutoPlaying(false)
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Sticky Header */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100 shadow-sm">
        <nav className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-blue-700 bg-clip-text text-transparent">
                Masterpost.io
              </span>
            </Link>

            {/* Navigation Links */}
            <div className="hidden md:flex space-x-8">
              <a href="#examples" className="text-gray-600 hover:text-blue-600 transition-colors">
                Examples
              </a>
              <a href="#pricing" className="text-gray-600 hover:text-blue-600 transition-colors">
                Pricing
              </a>
              <a href="#faq" className="text-gray-600 hover:text-blue-600 transition-colors">
                FAQ
              </a>
            </div>

            {/* CTA Buttons */}
            <div className="flex items-center space-x-4">
              <Link href="/app" className="text-gray-600 hover:text-blue-600 transition-colors">
                Login
              </Link>
              <Link href="/app">
                <Button className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-lg shadow-blue-500/25">
                  Start Free
                </Button>
              </Link>
            </div>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-blue-50 via-white to-white py-20 overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-30" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-100 rounded-full blur-3xl opacity-30" />
        </div>

        <div className="container mx-auto px-6 relative z-10">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left Column: Copy */}
            <div className="space-y-8">
              <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold">
                <Star className="w-4 h-4 fill-current" />
                <span>Professional E-commerce Image Processing</span>
              </div>

              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight">
                Perfect Product Images in{" "}
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Seconds
                </span>
              </h1>

              <p className="text-xl text-gray-600 leading-relaxed">
                AI-powered background removal for Amazon, eBay & Instagram. From simple products to complex items with
                pixel-perfect edges.
              </p>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6">
                <div>
                  <div className="text-3xl font-bold text-blue-600">10K+</div>
                  <div className="text-sm text-gray-600">Images processed</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-blue-600">2-6s</div>
                  <div className="text-sm text-gray-600">Avg. time</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-blue-600">99.9%</div>
                  <div className="text-sm text-gray-600">Satisfaction</div>
                </div>
              </div>

              {/* CTAs */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/app">
                  <Button
                    size="lg"
                    className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-xl shadow-blue-500/25 text-lg px-8"
                  >
                    Process 10 Images Free
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </Button>
                </Link>
                <a href="#pricing">
                  <Button size="lg" variant="outline" className="border-2 border-blue-200 text-blue-700 text-lg px-8">
                    View Pricing
                  </Button>
                </a>
              </div>

              <p className="text-sm text-gray-500 flex items-center gap-4">
                <span className="flex items-center">
                  <Check className="w-4 h-4 text-green-600 mr-1" /> No credit card
                </span>
                <span className="flex items-center">
                  <Check className="w-4 h-4 text-green-600 mr-1" /> 10 free images
                </span>
                <span className="flex items-center">
                  <Check className="w-4 h-4 text-green-600 mr-1" /> Upgrade anytime
                </span>
              </p>
            </div>

            {/* Right Column: Visual Showcase */}
            <div className="relative">
              <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-gray-500 text-center uppercase tracking-wider">Before</p>
                    <div className="relative aspect-square rounded-xl overflow-hidden bg-gray-100">
                      <Image
                        src="/samples/original/bicicleta.jpg"
                        alt="Before processing"
                        fill
                        className="object-cover"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-gray-500 text-center uppercase tracking-wider">After</p>
                    <div className="relative aspect-square rounded-xl overflow-hidden bg-gray-100">
                      <Image
                        src="/samples/processed/bicicleta.jpg"
                        alt="After processing"
                        fill
                        className="object-cover"
                      />
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-100">
                  <Sparkles className="w-4 h-4 text-green-600" />
                  <span className="text-sm font-semibold text-green-700">Premium Quality • 6 seconds</span>
                </div>
              </div>

              {/* Floating badges */}
              <div className="absolute -top-4 -left-4 bg-white rounded-full shadow-lg px-4 py-2 flex items-center space-x-2">
                <Zap className="w-4 h-4 text-yellow-500 fill-current" />
                <span className="text-sm font-semibold">Fast Processing</span>
              </div>
              <div className="absolute -bottom-4 -right-4 bg-white rounded-full shadow-lg px-4 py-2 flex items-center space-x-2">
                <Shield className="w-4 h-4 text-blue-500" />
                <span className="text-sm font-semibold">Secure & Private</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Showcase Section - MOST IMPORTANT */}
      <section id="examples" className="py-20 bg-gradient-to-b from-white to-gray-50">
        <div className="container mx-auto px-6">
          {/* Section Header */}
          <div className="text-center mb-16 space-y-4">
            <Badge className="bg-purple-100 text-purple-700 hover:bg-purple-100">Premium Showcase</Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
              See the{" "}
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Premium Difference
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Complex items processed in seconds with our Premium AI. Perfect edges, zero shadows, pure white
              backgrounds.
            </p>
          </div>

          {/* New Gallery Showcase Component */}
          <GalleryShowcase />

          {/* Slider */}
          <div className="relative max-w-6xl mx-auto">
            <div className="overflow-hidden rounded-2xl">
              <div
                className="flex transition-transform duration-500 ease-out"
                style={{ transform: `translateX(-${currentSlide * 100}%)` }}
              >
                {GALLERY_ITEMS.map((item, index) => (
                  <div key={item.id} className="min-w-full">
                    <div className="bg-white rounded-2xl p-8 mx-2">
                      <div className="grid md:grid-cols-3 gap-6 items-center mb-6">
                        {/* Before */}
                        <div className="space-y-3">
                          <p className="text-sm font-bold text-gray-900 text-center uppercase tracking-wider">
                            Before
                          </p>
                          <div className="relative aspect-square rounded-xl overflow-hidden shadow-lg bg-gray-100">
                            <Image
                              src={`/samples/original/${item.id}.jpg`}
                              alt={`${item.title} - Original`}
                              fill
                              className="object-cover"
                            />
                          </div>
                        </div>

                        {/* Arrow */}
                        <div className="flex flex-col items-center justify-center space-y-3">
                          <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center shadow-lg">
                            <ArrowRight className="w-8 h-8 text-white" />
                          </div>
                          <div className="text-center">
                            <p className="text-sm font-semibold text-gray-900">Premium AI</p>
                            <p className="text-xs text-gray-500">{item.time} processing</p>
                          </div>
                        </div>

                        {/* After */}
                        <div className="space-y-3">
                          <p className="text-sm font-bold text-gray-900 text-center uppercase tracking-wider">After</p>
                          <div className="relative aspect-square rounded-xl overflow-hidden shadow-lg bg-white border border-gray-200">
                            <Image
                              src={`/samples/processed/${item.id}.jpg`}
                              alt={`${item.title} - Processed`}
                              fill
                              className="object-cover"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Description */}
                      <div className="text-center space-y-3 pt-4 border-t border-gray-100">
                        <h3 className="text-2xl font-bold text-gray-900">{item.title}</h3>
                        <div className="flex items-center justify-center gap-4 text-sm text-gray-600">
                          <span className="flex items-center">
                            <Check className="w-4 h-4 text-green-600 mr-1" />
                            {item.description}
                          </span>
                          <span className="flex items-center">
                            <Zap className="w-4 h-4 text-yellow-500 mr-1" />
                            {item.time}
                          </span>
                          <span className="flex items-center">
                            <Sparkles className="w-4 h-4 text-purple-600 mr-1" />
                            Premium AI
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Navigation Arrows */}
            <button
              onClick={prevSlide}
              className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-12 bg-white rounded-full p-4 shadow-xl hover:shadow-2xl hover:scale-110 transition-all"
              aria-label="Previous slide"
            >
              <ChevronLeft className="w-6 h-6 text-gray-900" />
            </button>

            <button
              onClick={nextSlide}
              className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-12 bg-white rounded-full p-4 shadow-xl hover:shadow-2xl hover:scale-110 transition-all"
              aria-label="Next slide"
            >
              <ChevronRight className="w-6 h-6 text-gray-900" />
            </button>

            {/* Dots Navigation */}
            <div className="flex justify-center mt-8 space-x-2">
              {GALLERY_ITEMS.map((_, index) => (
                <button
                  key={index}
                  onClick={() => goToSlide(index)}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentSlide ? "bg-blue-600 w-8" : "bg-gray-300 hover:bg-gray-400"
                  }`}
                  aria-label={`Go to slide ${index + 1}`}
                />
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="text-center mt-12">
            <Link href="/app">
              <Button
                size="lg"
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-xl shadow-purple-500/25 text-lg px-8"
              >
                Try Premium Quality Free
                <Sparkles className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <p className="text-sm text-gray-500 mt-3">Start with 10 free images • No credit card required</p>
          </div>
        </div>
      </section>

      {/* Comparison Section - Basic vs Premium */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900">Choose Your Quality</h2>
            <p className="text-xl text-gray-600">Basic for simple products, Premium for complex items</p>
          </div>

          <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-8">
            {/* Basic Card */}
            <Card className="border-2 border-gray-200 hover:border-gray-300 transition-all">
              <CardContent className="p-8 space-y-6">
                <div className="text-center space-y-2">
                  <Badge variant="outline" className="text-base">
                    BASIC
                  </Badge>
                  <div className="text-4xl font-bold text-gray-900">$0.10</div>
                  <p className="text-gray-600">per image</p>
                </div>

                <div className="space-y-3">
                  {[
                    "Good for simple backgrounds",
                    "Fast processing (~2 seconds)",
                    "Cost-effective for bulk",
                    "No watermark",
                  ].map((feature, i) => (
                    <div key={i} className="flex items-start">
                      <Check className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>

                <div className="pt-6 border-t border-gray-100">
                  <p className="text-sm font-semibold text-gray-900 mb-2">Best for:</p>
                  <p className="text-sm text-gray-600">Clothing, simple objects, high-volume processing</p>
                </div>
              </CardContent>
            </Card>

            {/* Premium Card */}
            <Card className="border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-pink-50 relative overflow-hidden">
              <div className="absolute top-4 right-4">
                <Badge className="bg-gradient-to-r from-purple-600 to-pink-600 text-white">RECOMMENDED</Badge>
              </div>

              <CardContent className="p-8 space-y-6">
                <div className="text-center space-y-2">
                  <Badge variant="outline" className="text-base border-purple-300 text-purple-700">
                    PREMIUM
                  </Badge>
                  <div className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                    $0.30
                  </div>
                  <p className="text-gray-600">per image</p>
                </div>

                <div className="space-y-3">
                  {[
                    "Perfect for complex items",
                    "Zero shadows, pure white",
                    "Professional e-commerce quality",
                    "Glass, metal, reflective surfaces",
                    "Fine details preserved",
                  ].map((feature, i) => (
                    <div key={i} className="flex items-start">
                      <Check className="w-5 h-5 text-purple-600 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700 font-medium">{feature}</span>
                    </div>
                  ))}
                </div>

                <div className="pt-6 border-t border-purple-100">
                  <p className="text-sm font-semibold text-gray-900 mb-2">Best for:</p>
                  <p className="text-sm text-gray-700">Jewelry, glass, complex products, hero images</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="mt-12 max-w-2xl mx-auto">
            <div className="bg-blue-50 rounded-xl p-6 border border-blue-100">
              <p className="text-center text-gray-700">
                <span className="font-semibold">💡 Pro Tip:</span> Use Basic for bulk simple products, Premium for
                your hero products and complex items
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gradient-to-b from-gray-50 to-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 space-y-4">
            <Badge className="bg-green-100 text-green-700 hover:bg-green-100">Simple Pricing</Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
              Pay Only for{" "}
              <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                What You Use
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Start free, scale as you grow. No subscriptions, no hidden fees.
            </p>
          </div>

          <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
            {/* FREE Plan */}
            <Card className="border-2 border-gray-200 hover:border-gray-300 transition-all">
              <CardContent className="p-8 space-y-6">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold text-gray-900">FREE</h3>
                  <div className="flex items-baseline">
                    <span className="text-5xl font-bold text-gray-900">$0</span>
                  </div>
                  <p className="text-gray-600">10 credits included</p>
                </div>

                <div className="py-4">
                  <div className="bg-green-50 border border-green-100 rounded-lg p-4 space-y-1">
                    <p className="text-sm font-semibold text-green-900">You get:</p>
                    <p className="text-sm text-green-700">✓ 10 Basic images</p>
                    <p className="text-xs text-green-600">OR 3 Premium images + 1 Basic</p>
                  </div>
                </div>

                <div className="space-y-3">
                  {[
                    "No credit card required",
                    "All marketplace formats",
                    "Amazon, eBay, Instagram",
                    "Batch processing",
                    "ZIP download",
                  ].map((feature, i) => (
                    <div key={i} className="flex items-start">
                      <Check className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>

                <Link href="/app" className="block">
                  <Button className="w-full" variant="outline">
                    Start Free
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* PRO PACK - Most Popular */}
            <Card className="border-2 border-blue-500 shadow-xl relative scale-105 bg-gradient-to-br from-blue-50 to-indigo-50">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                <Badge className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-1.5 text-sm font-bold">
                  MOST POPULAR
                </Badge>
              </div>

              <CardContent className="p-8 space-y-6 mt-4">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold text-gray-900">PRO PACK</h3>
                  <div className="flex items-baseline">
                    <span className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                      $17.99
                    </span>
                  </div>
                  <p className="text-gray-600">200 credits included</p>
                </div>

                <div className="py-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-1">
                    <p className="text-sm font-semibold text-blue-900">You get:</p>
                    <p className="text-sm text-blue-700">✓ 200 Basic images</p>
                    <p className="text-sm text-blue-700">✓ 66 Premium images</p>
                    <p className="text-xs text-blue-600">Or any combination (1 Basic = 1 credit, 1 Premium = 3 credits)</p>
                  </div>
                </div>

                <div className="space-y-3">
                  {[
                    "Everything in Free",
                    "Premium AI processing",
                    "Priority support",
                    "Bulk discounts",
                    "Credits never expire",
                    "Commercial license",
                  ].map((feature, i) => (
                    <div key={i} className="flex items-start">
                      <Check className="w-5 h-5 text-blue-600 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700 font-medium">{feature}</span>
                    </div>
                  ))}
                </div>

                <Link href="/app" className="block">
                  <Button className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg">
                    Get Pro Pack
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* BUSINESS PACK */}
            <Card className="border-2 border-purple-200 hover:border-purple-300 transition-all bg-gradient-to-br from-purple-50 to-pink-50">
              <CardContent className="p-8 space-y-6">
                <div className="space-y-2">
                  <h3 className="text-2xl font-bold text-gray-900">BUSINESS PACK</h3>
                  <div className="flex items-baseline">
                    <span className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                      $39.99
                    </span>
                  </div>
                  <p className="text-gray-600">500 credits included</p>
                </div>

                <div className="py-4">
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 space-y-1">
                    <p className="text-sm font-semibold text-purple-900">You get:</p>
                    <p className="text-sm text-purple-700">✓ 500 Basic images</p>
                    <p className="text-sm text-purple-700">✓ 166 Premium images</p>
                    <p className="text-xs text-purple-600">Best value for high-volume sellers</p>
                  </div>
                </div>

                <div className="space-y-3">
                  {[
                    "Everything in Pro Pack",
                    "Maximum value per credit",
                    "Volume processing",
                    "API access (coming soon)",
                    "Dedicated support",
                    "Custom pipelines",
                  ].map((feature, i) => (
                    <div key={i} className="flex items-start">
                      <Check className="w-5 h-5 text-purple-600 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700 font-medium">{feature}</span>
                    </div>
                  ))}
                </div>

                <Link href="/app" className="block">
                  <Button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white">
                    Get Business Pack
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>

          {/* Credit System Explanation */}
          <div className="mt-16 max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white shadow-2xl">
              <h3 className="text-2xl font-bold mb-6 text-center">How Credits Work</h3>
              <div className="grid md:grid-cols-2 gap-8">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 space-y-3">
                  <div className="text-3xl font-bold">1 Credit</div>
                  <div className="text-xl">= 1 Basic Image</div>
                  <p className="text-sm text-blue-100">Good quality, fast processing (~2s)</p>
                  <div className="text-sm font-semibold">$0.10 per image</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 space-y-3">
                  <div className="text-3xl font-bold">3 Credits</div>
                  <div className="text-xl">= 1 Premium Image</div>
                  <p className="text-sm text-purple-100">Premium AI quality (~5s)</p>
                  <div className="text-sm font-semibold">$0.30 per image</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 space-y-4">
            <Badge className="bg-gray-100 text-gray-700 hover:bg-gray-100">FAQ</Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900">Frequently Asked Questions</h2>
            <p className="text-xl text-gray-600">Everything you need to know about Masterpost.io</p>
          </div>

          <div className="max-w-3xl mx-auto space-y-4">
            {[
              {
                question: "What's the difference between Basic and Premium?",
                answer:
                  "Basic uses local AI processing (rembg) and is perfect for simple products with solid backgrounds. Premium uses our advanced Qwen AI for complex items like jewelry, glass, or reflective surfaces - giving you pixel-perfect edges and zero shadows.",
              },
              {
                question: "How does the credit system work?",
                answer:
                  "1 credit = 1 Basic image ($0.10), 3 credits = 1 Premium image ($0.30). You can mix and match as needed. For example, with 200 credits (Pro Pack), you can process 200 Basic images OR 66 Premium images OR any combination.",
              },
              {
                question: "Do credits expire?",
                answer:
                  "No! Once you purchase a pack, your credits never expire. Use them at your own pace. This makes our packs perfect for seasonal sellers or variable workloads.",
              },
              {
                question: "Can I process images in bulk?",
                answer:
                  "Absolutely! You can upload multiple images at once and process them all in one batch. All results are packaged into a convenient ZIP file for download. Perfect for e-commerce sellers with large catalogs.",
              },
              {
                question: "What image formats do you support?",
                answer:
                  "We accept JPG, JPEG, PNG, and WEBP for input. Output is always high-quality JPG with pure white backgrounds, optimized for Amazon, eBay, and Instagram requirements.",
              },
              {
                question: "How long are images stored?",
                answer:
                  "Processed images are stored for 24 hours, giving you plenty of time to download them. After that, they're automatically deleted for your privacy. We recommend downloading your ZIP file immediately after processing.",
              },
              {
                question: "Is my data secure and private?",
                answer:
                  "Yes! We use secure HTTPS connections, your images are automatically deleted after 24 hours, and we never share your data with third parties. Your intellectual property is safe with us.",
              },
              {
                question: "Can I upgrade or buy more credits anytime?",
                answer:
                  "Yes! You can purchase additional credit packs anytime. Credits from different purchases stack together and never expire. Start with the Free tier and upgrade whenever you need more.",
              },
            ].map((faq, index) => (
              <div key={index} className="border border-gray-200 rounded-xl overflow-hidden hover:border-blue-300 transition-colors">
                <button
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  className="w-full px-6 py-5 flex items-center justify-between bg-white hover:bg-gray-50 transition-colors text-left"
                >
                  <span className="font-semibold text-gray-900 text-lg pr-4">{faq.question}</span>
                  <ChevronDown
                    className={`w-5 h-5 text-gray-500 flex-shrink-0 transition-transform ${
                      openFaq === index ? "rotate-180" : ""
                    }`}
                  />
                </button>
                {openFaq === index && (
                  <div className="px-6 py-5 bg-gray-50 border-t border-gray-200">
                    <p className="text-gray-700 leading-relaxed">{faq.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Still have questions CTA */}
          <div className="mt-16 text-center">
            <p className="text-gray-600 mb-4">Still have questions?</p>
            <Link href="/app">
              <Button variant="outline" className="border-2 border-blue-200 text-blue-700">
                Contact Support
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl" />
        </div>

        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <h2 className="text-4xl md:text-6xl font-bold leading-tight">
              Ready to Transform Your Product Images?
            </h2>
            <p className="text-xl md:text-2xl text-blue-100">
              Join thousands of sellers creating professional e-commerce images in seconds
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link href="/app">
                <Button
                  size="lg"
                  className="bg-white text-blue-600 hover:bg-gray-100 shadow-2xl text-lg px-10 py-6 h-auto"
                >
                  Start Processing Free
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
              <p className="text-sm text-blue-100">No credit card • 10 free images • Upgrade anytime</p>
            </div>

            <div className="grid grid-cols-3 gap-8 pt-12 max-w-2xl mx-auto">
              <div>
                <div className="text-4xl font-bold">10K+</div>
                <div className="text-blue-100">Images processed</div>
              </div>
              <div>
                <div className="text-4xl font-bold">2-6s</div>
                <div className="text-blue-100">Average time</div>
              </div>
              <div>
                <div className="text-4xl font-bold">99.9%</div>
                <div className="text-blue-100">Satisfaction</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div className="space-y-4">
              <Link href="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">Masterpost.io</span>
              </Link>
              <p className="text-sm text-gray-400">Professional e-commerce image processing powered by AI</p>
            </div>

            {/* Product */}
            <div className="space-y-3">
              <h3 className="text-white font-semibold">Product</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#examples" className="hover:text-white transition-colors">
                    Examples
                  </a>
                </li>
                <li>
                  <a href="#pricing" className="hover:text-white transition-colors">
                    Pricing
                  </a>
                </li>
                <li>
                  <Link href="/app" className="hover:text-white transition-colors">
                    Dashboard
                  </Link>
                </li>
              </ul>
            </div>

            {/* Support */}
            <div className="space-y-3">
              <h3 className="text-white font-semibold">Support</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#faq" className="hover:text-white transition-colors">
                    FAQ
                  </a>
                </li>
                <li>
                  <Link href="/app" className="hover:text-white transition-colors">
                    Contact
                  </Link>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Documentation
                  </a>
                </li>
              </ul>
            </div>

            {/* Legal */}
            <div className="space-y-3">
              <h3 className="text-white font-semibold">Legal</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Terms of Service
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-white transition-colors">
                    Refund Policy
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-400">© 2025 Masterpost.io. All rights reserved.</p>
            <div className="flex items-center space-x-6">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">Twitter</span>
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">GitHub</span>
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    fillRule="evenodd"
                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                    clipRule="evenodd"
                  />
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <span className="sr-only">LinkedIn</span>
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}