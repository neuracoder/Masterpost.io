'use client'

import { useAuth } from '@/lib/auth-context'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function DashboardPage() {
  const { user, credits, loading, signOut, refreshCredits } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      refreshCredits()
    }
  }, [user])

  if (loading || !user) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-xl font-bold">Masterpost.io</h1>
            <div className="flex items-center gap-4">
              <span className="text-sm">
                Credits: <strong>{credits}</strong>
              </span>
              <button
                onClick={signOut}
                className="px-4 py-2 text-sm text-red-600 hover:text-red-800"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Welcome, {user.email}!</h2>
          
          <div className="mb-6">
            <p className="text-gray-600">Current Balance:</p>
            <p className="text-4xl font-bold text-blue-600">{credits} Credits</p>
          </div>

          {credits < 10 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded p-4 mb-6">
              <p className="text-yellow-800">
                You're running low on credits!
              </p>
            </div>
          )}

          <div className="space-y-4">
            <Link
              href="/pricing"
              className="block w-full text-center px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Buy More Credits
            </Link>
            
            <Link
              href="/"
              className="block w-full text-center px-4 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Process Images
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
