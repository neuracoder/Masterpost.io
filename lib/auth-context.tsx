'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface User {
  id: string
  email: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  credits: number
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string) => Promise<void>
  signOut: () => void
  refreshCredits: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [credits, setCredits] = useState<number>(0)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Cargar sesión del localStorage
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
      fetchCredits(savedToken)
    }
    setLoading(false)
  }, [])

  const fetchCredits = async (authToken: string) => {
    try {
      const response = await fetch(`${API_URL}/api/credits/balance`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setCredits(data.credits || 0)
      }
    } catch (error) {
      console.error('Error fetching credits:', error)
    }
  }

  const signIn = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) {
      throw new Error('Login failed')
    }

    const data = await response.json()
    setUser(data.user)
    setToken(data.access_token)
    
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    
    await fetchCredits(data.access_token)
    router.push('/dashboard')
  }

  const signUp = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) {
      throw new Error('Signup failed')
    }

    const data = await response.json()
    setUser(data.user)
    setToken(data.access_token)
    
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    
    await fetchCredits(data.access_token)
    router.push('/dashboard')
  }

  const signOut = () => {
    setUser(null)
    setToken(null)
    setCredits(0)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const refreshCredits = async () => {
    if (token) {
      await fetchCredits(token)
    }
  }

  return (
    <AuthContext.Provider value={{
      user,
      token,
      credits,
      loading,
      signIn,
      signUp,
      signOut,
      refreshCredits
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
