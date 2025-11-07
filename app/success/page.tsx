'use client'

import { useEffect } from 'react'
import { useAuth } from '@/lib/auth-context'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'

export default function SuccessPage() {
  const { refreshCredits, credits } = useAuth()
  const router = useRouter()
  const searchParams = useSearchParams()
  const sessionId = searchParams.get('session_id')

  useEffect(() => {
    if (sessionId) {
      // Actualizar créditos después de pago exitoso
      refreshCredits()
    } else {
      router.push('/pricing')
    }
  }, [sessionId])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow text-center">
        <div className="text-6xl">🎉</div>
        
        <div>
          <h2 className="text-3xl font-bold text-green-600 mb-2">
            Payment Successful!
          </h2>
          <p className="text-gray-600">
            Your credits have been added to your account
          </p>
        </div>

        <div className="bg-blue-50 rounded-lg p-6">
          <p className="text-sm text-gray-600 mb-2">New Balance:</p>
          <p className="text-4xl font-bold text-blue-600">{credits} Credits</p>
        </div>

        <div className="space-y-3">
          <Link
            href="/dashboard"
            className="block w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go to Dashboard
          </Link>
          
          <Link
            href="/"
            className="block w-full py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Start Processing Images
          </Link>
        </div>
      </div>
    </div>
  )
}
