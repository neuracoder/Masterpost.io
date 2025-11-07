'use client'

import { useAuth } from '@/lib/auth-context'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'

export default function PricingPage() {
  const { user, token } = useAuth()
  const [loading, setLoading] = useState<string | null>(null)
  const router = useRouter()

  const handlePurchase = async (packType: string) => {
    if (!user || !token) {
      router.push('/login')
      return
    }

    setLoading(packType)

    try {
      const response = await fetch(`${API_URL}/api/payments/create-checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ pack_type: packType })
      })

      if (!response.ok) {
        throw new Error('Failed to create checkout')
      }

      const data = await response.json()
      window.location.href = data.checkout_url
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to start checkout. Please try again.')
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Choose Your Credit Pack</h1>
          <p className="text-gray-600">
            Purchase credits to process your images
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* PRO Pack */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h3 className="text-2xl font-bold mb-2">Pro Pack</h3>
            <div className="text-4xl font-bold mb-4">$17.99</div>
            <p className="text-gray-600 mb-6">200 Credits</p>
            
            <ul className="space-y-3 mb-8">
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Process 200 images
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                $0.09 per credit
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                No expiration
              </li>
            </ul>

            <button
              onClick={() => handlePurchase('PRO')}
              disabled={loading === 'PRO'}
              className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading === 'PRO' ? 'Processing...' : 'Purchase Pro Pack'}
            </button>
          </div>

          {/* BUSINESS Pack */}
          <div className="bg-white rounded-lg shadow-lg p-8 border-2 border-blue-500 relative">
            <div className="absolute top-0 right-0 bg-blue-500 text-white px-3 py-1 text-sm rounded-bl">
              BEST VALUE
            </div>
            
            <h3 className="text-2xl font-bold mb-2">Business Pack</h3>
            <div className="text-4xl font-bold mb-4">$39.99</div>
            <p className="text-gray-600 mb-6">500 Credits</p>
            
            <ul className="space-y-3 mb-8">
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Process 500 images
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                $0.08 per credit
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                No expiration
              </li>
              <li className="flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                Priority support
              </li>
            </ul>

            <button
              onClick={() => handlePurchase('BUSINESS')}
              disabled={loading === 'BUSINESS'}
              className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading === 'BUSINESS' ? 'Processing...' : 'Purchase Business Pack'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
